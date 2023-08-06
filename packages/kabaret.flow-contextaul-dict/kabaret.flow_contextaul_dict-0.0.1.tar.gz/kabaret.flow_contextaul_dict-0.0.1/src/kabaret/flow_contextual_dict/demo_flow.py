'''
In this example we define a 'settings' contextual dict by declaring some 
Child relations to a ContextualDict with the name 'settings'.

At several levels of the DemoFlow (infinite) flow tree, the user can see, 
override and add values in the settings context.
Those objects (Branch1 and Branch2) implement the method:
`get_contextual_edits(self, context_name, keys=None)`
which returns a dict of edits for the branch. Those edit can be 
programatic or user-defined using a `ContextualEdits` object (or a 
combination of both, as seen in Branch2)

At other levels of the tree, we use values from this 'settings' 
contextual dict in ComputedParams to show how to retreive a sub set of
the dict (please note that this is not a speed optimisation).

Sometimes you want to confine the settings inside an child objet instead
of having them directly inside objects in the branch path.
The DemoFlow object here does that by having its `get_contextual_edits()`
method forwarding the call to `self.admin.get_contextual_edits()`.

''' 
from kabaret import flow

from . import ContextualView, ContextualEdits, get_contextual_dict


class SettingsReader(flow.Object):

    def compute_child_value(self, child_value):
        key = child_value.name()

        context = get_contextual_dict(
            leaf=self,
            context_name='settings',
            keys=[key]
        )

        child_value.set(
            'The current {} is "{}"'.format(
                key,
                context.get(key, '! NOT FOUND !')
            )
        )

class SettingsReader1(SettingsReader):

    fps = flow.Computed()
    path = flow.Computed()

class SettingsReader2(SettingsReader):

    fps = flow.Computed()
    pool = flow.Computed()
    
class SettingsView(ContextualView):
    '''
    The Settings view must know where to store
    edits. This class assumes there is a sibbling
    relation named "_setting_overrides" pointing to
    a ContextualEdits object and uses it.
    '''
    _parent = flow.Parent()

    def get_edit_map(self):
        return self._parent._setting_overrides

class Branch1(flow.Object):

    # This will relate to a Group
    # when the class is defined
    sub_tree = flow.Child(None)

    _setting_overrides = flow.Child(ContextualEdits)
    # The name of this relation must match the context_name:
    settings = flow.Child(SettingsView)

    settings_usage = flow.Child(SettingsReader1)

    def get_contextual_edits(self, context_name, keys=None):
        if context_name == 'settings':
            return self._setting_overrides.to_dict(keys)

class Branch2(flow.Object):

    # This will relate to a Group
    # when the class is defined
    sub_tree = flow.Child(None)

    _setting_overrides = flow.Child(ContextualEdits)
    # The name of this relation must match the context_name:
    settings = flow.Child(SettingsView)

    settings_usage = flow.Child(SettingsReader2)

    def get_contextual_edits(self, context_name, keys=None):
        if context_name == 'settings':
            context = self._setting_overrides.to_dict(keys)
            if context:
                context['oid'] = self.oid()
                return context

class Group(flow.Object):

    branch1 = flow.Child(Branch1) 
    branch2 = flow.Child(Branch2) 

# Configure Circular Relations
Branch1.sub_tree.set_related_type(Group)
Branch2.sub_tree.set_related_type(Group)


class ProjectAdmin(flow.Object):

    _setting_overrides = flow.Child(ContextualEdits)
    
    # the name of this relation drives the `context_name`
    # arg of `self.get_contextual_edits()`
    settings = flow.Child(SettingsView)

    def get_contextual_edits(self, context_name, keys=None):
        if context_name == 'settings':
            defaults = dict(
                fps=30,
                path='/DEFAULT/PATH/TO/STUFF',
                pool='render_nodes'
            )
            if keys is None:
                # returns the whole dict:
                return defaults.copy()
            else:
                return dict([
                    (k,defaults[k])
                    for k in keys 
                ])

class DemoFlow(flow.Object):

    tree = flow.Child(Group)
    admin = flow.Child(ProjectAdmin)

    def get_contextual_edits(self, context_name, keys=None):
        return self.admin.get_contextual_edits(context_name, keys)

'''
import kabaret.flow_contextual_dict.demo_flow
import importlib
importlib.reload(kabaret.flow_contextual_dict.demo_flow)


'''