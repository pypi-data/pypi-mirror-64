from __future__ import print_function

import traceback
from kabaret import flow


#
#   VIEW
#

class EditContextualValueAction(flow.Action):

    _view_map = flow.Parent(2)
    _view_item = flow.Parent()
    value = flow.Param()

    def allow_context(self, context):
        return context == 'Flow.map'

    def needs_dialog(self):
        return True
    
    def get_buttons(self):
        value_name = self._view_item.value_name.get()
        self.message.set(
            '<h2>Edit value for <b>{}</b></h2>'.format(
                value_name
            )
        )
        self.value.set(self._view_item.value.get())
        buttons = ['Save']
        if self._view_map.get_edit_map().has_edit(value_name):
            buttons.append('Restore Default')
        return buttons

    def run(self, button):
        edit_map = self._view_map.get_edit_map()

        if button == 'Restore Default':
            # ! beware, do not edit the view item, 
            # the one to modify is in the edit map !
            edit_map.remove_edit(
                self._view_item.value_name.get()
            )
            edit_map.touch()
            self._view_map.touch()

        elif button == 'Save':
            # ! beware, do not edit the view item, 
            # the one to modify is in the edit map !
            edit_map.set_edit(
                self._view_item.value_name.get(),
                self.value.get(),
            )
            edit_map.touch()
            self._view_map.touch()

        return self.get_result(goto=self._view_map._mng.parent.oid())

class AddEditAction(flow.Action):

    _view_map = flow.Parent()

    value_name = flow.Param().ui(label='Name')
    value = flow.Param()

    def needs_dialog(self):
        return True
    
    def get_buttons(self):
        self.message.set(
            'Enter the name and the value.' 
        )
        return ['Add Edit',]

    def run(self, button):
        if not button == 'Add Edit':
            return
        
        edit_map = self._view_map.get_edit_map()
        edit_map.set_edit(
            self.value_name.get(),
            self.value.get()
        )
        edit_map.touch()
        self._view_map.touch()

class ContextualViewItem(flow.SessionObject):

    edit = flow.Child(EditContextualValueAction)

    value_name = flow.Computed(cached=True).ui(label='name')
    value = flow.Param(None)

    def compute_child_value(self, child_value):
        if child_value is self.value_name:
            child_value.set(self.name())

class ContextualView(flow.DynamicMap):
    
    add_value = flow.Child(AddEditAction)
    @classmethod
    def mapped_type(cls):
        return ContextualViewItem

    def get_edit_map(self):
        '''
        Must return the ContextualEdit Map 
        used to edit thru this view.
        '''
        raise NotImplemented
    
    def mapped_names(self, page_num=0, page_size=None):
        print('MAPPED_NAME', self.oid)
        context = get_contextual_dict(
            self, 
            self.name(),    # The view name drives the context name
            keys=None,      # None => fetch all keys
        )
        edits = self.get_edit_map().to_dict()
        context.update(edits)

        self._mng.children.clear() # rebuild all to ensure item are updated
        self._cache = {}
        item_prefix = self.name()+'_'
        for i, (k,v) in enumerate(context.items()):
            attr_name = '{}{}'.format(item_prefix,i)
            self._cache[attr_name] = dict(name=k, value=v)

        names = sorted(self._cache.keys())
        return names

    def _configure_child(self, child):
        child.value_name.set(self._cache[child.name()]['name'])
        child.value.set(self._cache[child.name()]['value'])

    def columns(self):
        return ['Name', 'Value']
    
    def _fill_row_cells(self, row, item):
        row['Name'] = item.value_name.get()
        row['Value'] = item.value.get()

    def _fill_row_style(self, style, item, row):
        pass

    def row(self, item):
        '''
        Configure the double-click to edit the item instead of goto it
        '''
        oid, row = super(ContextualView, self).row(item)
        return item.edit.oid(), row

    # def set_edit(self, name, value):
    #     self.get_edit_map().set_edit(name, value)
    
    # def remove_edit(self, name):
    #     self.get_edit_map().remove_edit(name)

#
#   EDIT
#

# class ContextualEditsValue(flow.values.Value):
#     pass

class ContextualEditsItem(flow.Object):

    edit_map = flow.Parent()

    value_name = flow.Param('???').ui(editable=False)
    value = flow.Param().watched()

    def child_value_changed(self, value):
        self.edit_map.touch()

class ContextualEdits(flow.Map):
    
    MAX_EDIT_COUNT = 500

    @classmethod
    def mapped_type(cls):
        return ContextualEditsItem

    def columns(self):
        return ['Name', 'Value']
    
    def _fill_row_cells(self, row, item):
        row['Name'] = item.value_name.get()
        row['Value'] = item.value.get()

    def to_dict(self, keys=None):
        '''
        If keys is not None, it must be a list of 
        value names to return
        '''
        edits = {}
        for item in self.mapped_items():
            value_name = item.value_name.get()
            if keys is None or value_name in keys:
                edits[value_name] = item.value.get()
        return edits
    
    def has_edit(self, name):
        for item in self.mapped_items():
            if item.value_name.get() == name:
                return True
        return False

    def set_edit(self, name, value):
        for item in self.mapped_items():
            if item.value_name.get() == name:
                item.value.set(value)
                return

        # item not found, create a new one:

        item_name = None
        names = self.mapped_names()
        for i in range(self.MAX_EDIT_COUNT):
            test_name = 'Item{}'.format(i)
            if test_name not in names:
                item_name = test_name
                break
        if item_name is None:
            raise Exception('Too many edits here, I wont allow more.')
        item = self.add(item_name)
        item.value_name.set(name)
        item.value.set(value)

    def remove_edit(self, name):
        for item in self.mapped_items():
            if item.value_name.get() == name:
                self.remove(item.name())
                return
        raise ValueError('Edit for "{}" not found.'.format(name))

#
#   FUNCTIONS
#

def get_contextual_dict(leaf, context_name, keys=None):
    parent = leaf._mng.parent
    if parent is None:
        context = dict()
    else:
        context = get_contextual_dict(parent, context_name, keys)

    try:
        get_edits = getattr(leaf, 'get_contextual_edits')
    except AttributeError:
        pass
    else:
        try:
            edits = get_edits(context_name, keys)
        except Exception as err:
            context['ERROR at '+leaf.oid()] = traceback.format_exc()
        else:
            # get_contextual_edits is allowed to return None:
            if edits:
                context.update(edits)
    
    return context
