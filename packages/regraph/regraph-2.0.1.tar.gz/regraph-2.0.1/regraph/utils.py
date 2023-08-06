"""A collection of utils for ReGraph library."""
import copy

from regraph.command_parser import parser
from regraph.exceptions import ReGraphError, ParsingError, RewritingError
from regraph.attribute_sets import AttributeSet, FiniteSet


def set_attrs(old_attrs, attrs, normalize=True, update=True):
    if normalize:
        normalize_attrs(attrs)

    for key in attrs:
        old_attrs[key] = attrs[key]
    if update:
        keys_to_remove = set()
        for key in old_attrs:
            if key not in attrs:
                keys_to_remove.add(key)
        for key in keys_to_remove:
            del old_attrs[key]
    return old_attrs


def add_attrs(old_attrs, attrs, normalize=True):
    if normalize:
        normalize_attrs(attrs)
    for key in attrs:
        if key in old_attrs:
            old_attrs[key] = old_attrs[key].union(attrs[key])
        else:
            old_attrs[key] = attrs[key]


def remove_attrs(old_attrs, attrs, normalize=True):
    if normalize:
        normalize_attrs(attrs)
    for key, value in attrs.items():
        if key in old_attrs:
            new_set = old_attrs[key].difference(value)
            if not new_set:
                del old_attrs[key]
            else:
                old_attrs[key] = new_set


def assign_attrs(element, attrs):
    for k, v in attrs.items():
        element[k] = v


def merge_attrs(original_dict, attrs):
    """Add attrs to the container."""
    if attrs is not None:
        normalize_attrs(attrs)
    else:
        attrs = dict()
    if original_dict is None:
        original_dict = attrs
    else:
        for key in attrs:
            if key in original_dict:
                original_dict[key] = original_dict[key].union(attrs[key])
            else:
                original_dict[key] = attrs[key]
    return


def safe_deepcopy_dict(d):
    """Util for safe deepcopy of a dict.

    Solves the issue with 'TypeError: can't pickle dict_items objects'
    of the default 'copy.deepcopy'.
    """
    try:
        new_d = copy.deepcopy(d)
    except TypeError:
        new_d = dict()
        for k, v in d.items():
            new_d[k] = copy.deepcopy(list(v.items()))
    return new_d


def generate_new_id(collection, basename):
    """Generate unique id for a node."""
    node_id = basename
    i = 1
    while node_id in collection:
        node_id = "{}_{}".format(basename, i)
        i += 1
    return node_id


def attrs_to_json(attrs):
    """Convert attributes to json."""
    normalize_attrs(attrs)
    json_data = dict()
    if attrs is not None:
        for key, value in attrs.items():
            json_data[key] = value.to_json()
    return json_data


def attrs_from_json(json_data):
    """Retrieve attrs from json-like dict."""
    attrs = dict()
    for key, value in json_data.items():
        attrs[key] = AttributeSet.from_json(value)
    return attrs


def relation_to_json(rel):
    """Convert relation to json-serializable."""
    json_data = {}
    for k, v in rel.items():
        json_data[k] = list(v)
    return json_data


def load_nodes_from_json(j_data):
    """Load nodes from json-like dict."""
    loaded_nodes = []
    if "nodes" in j_data.keys():
        j_nodes = j_data["nodes"]
        for node in j_nodes:
            if "id" in node.keys():
                node_id = node["id"]
            else:
                raise ReGraphError(
                    "Error loading graph: node id is not specified!")
            attrs = None
            if "attrs" in node.keys():
                attrs = json_dict_to_attrs(node["attrs"])
            loaded_nodes.append((node_id, attrs))
    else:
        raise ReGraphError(
            "Error loading graph: no nodes specified!")
    return loaded_nodes


def load_edges_from_json(j_data):
    """Load edges from json-like dict."""
    loaded_edges = []
    if "edges" in j_data.keys():
        j_edges = j_data["edges"]
        for edge in j_edges:
            if "from" in edge.keys():
                s_node = edge["from"]
            else:
                raise ReGraphError(
                    "Error loading graph: edge source is not specified!")
            if "to" in edge.keys():
                t_node = edge["to"]
            else:
                raise ReGraphError(
                    "Error loading graph: edge target is not specified!")
            if "attrs" in edge.keys():
                attrs = json_dict_to_attrs(edge["attrs"])
                loaded_edges.append((s_node, t_node, attrs))
            else:
                loaded_edges.append((s_node, t_node))
    return loaded_edges


def json_dict_to_attrs(d):
    """Convert json dictionary to attributes."""
    attrs = {}
    for k, v in d.items():
        if "strSet" in v.keys() or "numSet" in v.keys():
            new_v = {
                "type": "FiniteSet",
                "data": []
            }
            if "pos_list" in v["strSet"].keys():
                new_v["data"].append(v["strSet"]["pos_list"])
            if "pos_list" in v["numSet"].keys():
                new_v["data"].append(v["numSet"]["pos_list"])
            v = new_v
        attrs[k] = AttributeSet.from_json(v)
    return attrs


def valid_attributes(source, target):
    """Test the validity of attributes."""
    for key, value in source.items():
        if key not in target:
            return False
        if not value.issubset(target[key]):
            return False
    return True


def is_subdict(small_dict, big_dict):
    """Check if the dictionary is a subset of other."""
    normalize_attrs(small_dict)
    normalize_attrs(big_dict)
    if small_dict is None:
        return True
    if len(small_dict) == 0:
        return True
    if all([len(v) == 0 for k, v in small_dict.items()]):
        return True
    if big_dict is None and len(small_dict) != 0:
        return False
    if len(big_dict) == 0 and len(small_dict) != 0:
        return False
    for key, value in small_dict.items():
        if key not in big_dict.keys():
            return False
        else:
            if not value.issubset(big_dict[key]):
                return False
    return True


def attrs_intersection(attrs1, attrs2):
    """Intersect two dictionaries with attrbutes."""
    if attrs1 is None or attrs2 is None:
        return {}
    res = dict()
    for key in attrs1.keys():
        if key in attrs2.keys():
            new_set = attrs1[key].intersection(attrs2[key])
            if new_set:
                res[key] = new_set
    return res


def attrs_union(attrs1, attrs2):
    """Find a union of two dictionaries with attrs."""
    if attrs1 is None:
        if attrs2 is not None:
            return attrs2
        else:
            return {}

    if attrs2 is None:
        return attrs1

    res = dict()
    for key in attrs1:
        if key in attrs2:
            res[key] = attrs1[key].union(attrs2[key])
        else:
            res[key] = attrs1[key]
    for key in attrs2:
        if key not in attrs1:
            res[key] = attrs2[key]
    return res


def keys_by_value(dictionary, val):
    """Get keys of a dictionary by a value."""
    res = []
    for key, value in dictionary.items():
        if value == val:
            res.append(key)
    return res


def fold_left(f, init, l):
    """ f : a -> b -> b
        init : b
        l : a list
        Returns f(...f(l[1],f(l[0], init)) """
    res = init
    for x in l:
        res = f(x, res)
    return res


def to_set(value):
    """Convert a value to set."""
    if type(value) == set or type(value) == list:
        return set(value)
    else:
        return set([value])


def to_list(value):
    """Convert a value to list."""
    if type(value) == set | type(value == list):
        return list(value)
    else:
        return [value]


def normalize_attrs(attrs):
    """Normalize node attributes."""
    if attrs is not None:
        for k, v in list(attrs.items()):
            if not isinstance(v, AttributeSet):
                attrs[k] = FiniteSet(v)
                if attrs[k].is_empty():
                    del attrs[k]
    return


def normalize_relation(relation):
    new_relation_dict = dict()
    for key, values in relation.items():
        if type(values) == set:
            new_relation_dict[key] = values
        elif type(values) == str:
            new_relation_dict[key] = {values}
        else:
            try:
                new_set = set()
                for v in values:
                    new_set.add(v)
                new_relation_dict[key] = new_set
            except TypeError:
                new_relation_dict[key] = {values}
    relation = new_relation_dict
    return new_relation_dict


def merge_attributes(attr1, attr2, method="union"):
    """Merge two dictionaries of attributes."""
    if method == "union":
        return attrs_union(attr1, attr2)
    elif method == "intersection":
        return attrs_intersection(attr1, attr2)
    else:
        raise ReGraphError("Merging method %s is not defined!" % method)


def dict_sub(attrs1, attrs2):
    """Remove attributes `attrs2` from `attrs1`."""
    new_dict = {}
    for key in attrs1:
        if key in attrs2:
            new_set = attrs1[key].difference(attrs2[key])
            if new_set:
                new_dict[key] = new_set
        else:
            new_dict[key] = attrs1[key]
    return new_dict


def simplify_commands(commands, di=False):
    """Simplify a list of graph transformation commands."""
    command_strings = [c for c in commands.splitlines() if len(c) > 0]
    actions = []
    for command in command_strings:
        try:
            print(command)
            parsed = parser.parseString(command).asDict()
            actions.append(parsed)
        except:
            raise ParsingError("Cannot parse command '%s'" % command)

    # We keep updated a list of the element we added, the lines of
    # transformations that added them or added attributes to them
    # and the type of addition we did (node or edge)

    added = []
    ad_index = []
    ad_type = []

    # We keep updated a list of the element we deleted and the lines of
    # transformation that deleted them or deleted attributes from them

    deleted = []
    del_index = []

    # We keep updated a list of the element we cloned and the line of
    # transformation that cloned them

    cloned = []
    clone_index = []

    # List of elements to remove at the end

    elements_to_remove = []

    # For each line of command we change what to remove and what to keep
    # We update the lists at each step, the only operations that actually
    # do simplify the commands are the deletion of nodes and edges and the
    # merges. They try to find the all the operations they can remove
    # without changing the behaviour

    for i in range(len(actions)):
        action = actions[i]
        if action["keyword"] == "add_node":
            added.append(action["node"])
            ad_index.append([i])
            ad_type.append("node")
        elif action["keyword"] == "delete_node":
            if action["node"] not in cloned:
                # If the node haven't been cloned before
                rem_el = []
                for j in range(len(added)):
                    el = added[j]
                    if (type(el) == tuple and (el[0] == action["node"] or
                                               el[1] == action["node"])) or\
                       el == action["node"]:
                        # If the node have been involved in an addition
                        # we remove that addition since it has been
                        # deleted now, if there are not more lines that
                        # refers to the addition of that node, we can
                        # remove the deletion of the node
                        # Finding the node in added is not enough to
                        # remove the deletion since it can be an
                        # addition of an edge, we have to check if it
                        # the node itself that we added
                        if el == action["node"]:
                            elements_to_remove.append(i)
                        for k in ad_index[j]:
                            elements_to_remove.append(k)
                        rem_el.append(j)
                k = 0
                for j in rem_el:
                    del added[j - k]
                    del ad_index[j - k]
                    del ad_type[j - k]
                    k += 1
                rem_el = []
                for j in range(len(deleted)):
                    el = deleted[j]
                    if (type(el) == tuple and (el[0] == action["node"] or
                                               el[1] == action["node"])) or\
                       el == action["node"]:
                        # If the node have been involved in a deletion
                        # we can remove that deletion since the deletion
                        # of the node itself will delete what the deletion
                        # would have deleted
                        for k in del_index[j]:
                            elements_to_remove.append(k)
                        rem_el.append(j)
                k = 0
                for j in rem_el:
                    del deleted[j - k]
                    del del_index[j - k]
                    k += 1
            else:
                # If the node have been cloned before, we can't delete the
                # transformations that happened before the cloning since
                # they affected the clones too. We do so by comparing the
                # line of the transformation we are looking at and the line
                # of the last cloning operation that happened
                rem_el = []
                ind = max([clone_index[i] for i in range(
                    len(cloned)) if cloned[i] == action["node"]])
                for j in range(len(added)):
                    el = added[j]
                    if (type(el) == tuple and (el[0] == action["node"] or
                                               el[1] == action["node"])) or\
                            el == action["node"]:
                        rem_ind = []
                        for k in ad_index[j]:
                            if k > ind:
                                elements_to_remove.append(k)
                                rem_ind.append(k)
                        if ad_index[j] == rem_ind:
                            rem_el.append(j)
                        else:
                            for k in rem_ind:
                                ad_index[j].remove(k)
                m = 0
                for j in rem_el:
                    del added[j - m]
                    del ad_index[j - m]
                    del ad_type[j - m]
                    m += 1
                rem_el = []
                for j in range(len(deleted)):
                    el = deleted[j]
                    if (type(el) == tuple and (el[0] == action["node"] or
                                               el[1] == action["node"])) or\
                            el == action["node"]:
                        rem_ind = []
                        for k in del_index[j]:
                            if k > ind:
                                elements_to_remove.append(k)
                                rem_ind.append(k)
                        if del_index[j] == rem_ind:
                            rem_el.append(j)
                        else:
                            for k in rem_ind:
                                del_index[j].remove(k)
                m = 0
                for j in rem_el:
                    del deleted[j - m]
                    del del_index[j - m]
                    m += 1
                ind = clone_index.index(ind)
                del cloned[ind]
                del clone_index[ind]
            deleted.append(action["node"])
            del_index.append([i])
        elif action["keyword"] == "add_node_attrs":
            if action["node"] in added:
                j = added.index(action["node"])
                ad_index[j].append(i)
            else:
                added.append(action["node"])
                ad_index.append([i])
                ad_type.append("node_attrs")
        elif action["keyword"] == "delete_node_attrs":
            if action["node"] in deleted:
                j = deleted.index(action["node"])
                del_index[j].append(i)
            else:
                deleted.append(action["node"])
                del_index.append([i])
        elif action["keyword"] == "add_edge":
            e = (action["node_1"], action["node_2"])
            added.append(e)
            ad_index.append([i])
            ad_type.append("edge")
        elif action["keyword"] == "delete_edge":
            # It is the same idea as in the delete_node function, but with
            # a little bit more complexity since we have two nodes that
            # can possibly be cloned.
            # This time, finding the edge in the added list automatically
            # means we have to remove the deletion and the addition in the
            # case we didn't clone any of our nodes
            e = (action["node_1"], action["node_2"])
            if e[0] not in cloned and e[1] not in cloned:
                rem_el = []
                for j in range(len(added)):
                    el = added[j]
                    if type(el) == tuple and\
                       (el == e or (not di and el == (e[1], e[0]))):
                        elements_to_remove.append(i)
                        for k in ad_index[j]:
                            elements_to_remove.append(k)
                        rem_el.append(j)
                k = 0
                for j in rem_el:
                    del added[j - k]
                    del ad_index[j - k]
                    del ad_type[j - k]
                    k += 1
                rem_el = []
                for j in range(len(deleted)):
                    el = deleted[j]
                    if type(el) == tuple and\
                       (el == e or (not di and el == (e[1], e[0]))):
                        for k in del_index[j]:
                            elements_to_remove.append(k)
                        rem_el.append(j)
                k = 0
                for j in rem_el:
                    del deleted[j - k]
                    del del_index[j - k]
                    k += 1
            else:
                # Same idea as before if one of the nodes have been cloned,
                # but we have to take the max of the line number of all the
                # cloning operation on node 0 and node 1
                ind = 0
                if e[0] in cloned:
                    ind = max([clone_index[i]
                               for i in range(len(cloned)) if cloned[i] == e[0]])
                if e[1] in cloned:
                    ind = max([ind] + [clone_index[i]
                                       for i in range(len(cloned)) if cloned[i] == e[1]])

                ind = clone_index.index(ind)

                if e[0] in cloned:
                    rem_el = []
                    for j in range(len(added)):
                        el = added[j]
                        if type(el) == tuple and\
                           (el == e or (not di and el == (e[1], e[0]))):
                            rem_ind = []
                            for k in ad_index[j]:
                                if k > clone_index[ind]:
                                    elements_to_remove.append(k)
                                    # We remove the delete_edge operation
                                    # iff the same edge have been added
                                    # after the last cloning operation
                                    if ad_type[j] == "edge":
                                        elements_to_remove.append(i)
                                    rem_ind.append(k)
                            if ad_index[j] == rem_ind:
                                rem_el.append(j)
                            else:
                                for k in rem_ind:
                                    ad_index[j].remove(k)
                    m = 0
                    for j in rem_el:
                        del added[j - m]
                        del ad_index[j - m]
                        del ad_type[j - m]
                        m += 1
                    rem_el = []
                    for j in range(len(deleted)):
                        el = deleted[j]
                        if type(el) == tuple and\
                           (el == e or (not di and el == (e[1], e[0]))):
                            rem_ind = []
                            for k in del_index[j]:
                                if k > clone_index[ind]:
                                    elements_to_remove.append(k)
                                    rem_ind.append(k)
                            if del_index[j] == rem_ind:
                                rem_el.append(j)
                            else:
                                for k in rem_ind:
                                    del_index[j].remove(k)
                    m = 0
                    for j in rem_el:
                        del deleted[j - m]
                        del del_index[j - m]
                        m += 1
                if e[1] in cloned:
                    rem_el = []
                    for j in range(len(added)):
                        el = added[j]
                        if type(el) == tuple and\
                           (el == e or (not di and el == (e[1], e[0]))):
                            rem_ind = []
                            for k in ad_index[j]:
                                if k > clone_index[ind]:
                                    elements_to_remove.append(k)
                                    if ad_type[j] == "edge":
                                        elements_to_remove.append(i)
                                    rem_ind.append(k)
                            if ad_index[j] == rem_ind:
                                rem_el.append(j)
                            else:
                                for k in rem_ind:
                                    ad_index[j].remove(k)
                    m = 0
                    for j in rem_el:
                        del added[j - m]
                        del ad_index[j - m]
                        del ad_type[j - m]
                        m += 1
                    rem_el = []
                    for j in range(len(deleted)):
                        el = deleted[j]
                        if type(el) == tuple and\
                           (el == e or (not di and el == (e[1], e[0]))):
                            rem_ind = []
                            for k in del_index[j]:
                                if k > clone_index[ind]:
                                    elements_to_remove.append(k)
                                    rem_ind.append(k)
                            if del_index[j] == rem_ind:
                                rem_el.append(j)
                            else:
                                for k in rem_ind:
                                    del_index[j].remove(k)
                    m = 0
                    for j in rem_el:
                        del deleted[j - m]
                        del del_index[j - m]
                        m += 1
            deleted.append(e)
            del_index.append([i])
        elif action["keyword"] == "add_edge_attrs":
            e = (action["node_1"], action["node_2"])
            if e in added:
                j = added.index(e)
                ad_index[j].append(i)
            elif not di and (e[1], e[0]) in added:
                j = added.index((e[1], e[0]))
                ad_index[j].append(i)
            else:
                added.append(e)
                ad_index.append([i])
                ad_type.append("edge_attrs")
        elif action["keyword"] == "delete_edge_attrs":
            e = (action["node_1"], action["node_2"])
            if e in deleted:
                j = deleted.index(e)
                del_index[j].append(i)
            elif not di and (e[1], e[0]) in deleted:
                j = deleted.index((e[1], e[0]))
                del_index[j].append(i)
            else:
                deleted.append(e)
                del_index.append([i])
        elif action["keyword"] == "clone":
            if "node_name" in action.keys():
                added.append(action["node_name"])
                ad_index.append([i])
                ad_type.append("node")
            cloned.append(action["node"])
            clone_index.append(i)
        elif action["keyword"] == "merge":
            if "node_name" in action.keys():
                node_name = action["node_name"]
            else:
                node_name = "_".join(action["nodes"])

            added.append(node_name)
            ad_index.append([i])
            ad_type.append("node")

    return "\n".join(
        [command_strings[i]
         for i in range(len(actions))
         if i not in elements_to_remove])


def make_canonical_commands(g, commands, di=False):
    """Convert commands to the canonical form.

    Takes commands and the graph it refers to and returns a list of
    canonical transformations that have the same behaviour.
    The canonical form of a transformation follows this pattern :
    DELETIONS (DELETE_NODE, DELETE_NODE_ATTRS, DELETE_EDGE,
    DELETE_EDGE_ATTRS) CLONING (CLONE)
    ADDING and MERGING (ADD_NODE, ADD_NODE_ATTRS, ADD_EDGE,
    ADD_EDGE_ATTRS, MERGE)
    """
    res = []

    # We do multiple steps of simplification, until we found a fixed-point

    aux = commands
    next_step = simplify_commands(commands, di)
    while next_step != aux:
        aux = next_step
        next_step = simplify_commands(aux, di)

    # We keep updated an environment with our nodes and our edges

    env_nodes = [n for n in g.nodes()]
    env_edges = [e for e in g.edges()]

    if not di:
        for e in g.edges():
            if not (e[1], e[0]) in env_edges:
                env_edges.append((e[1], e[0]))

    # For each transformation we choose if we do it in this step or if we
    # keep it for later

    while next_step != '':
        command_strings = [c for c in next_step.splitlines() if len(c) > 0]
        actions = []
        for command in command_strings:
            try:
                parsed = parser.parseString(command).asDict()
                actions.append(parsed)
            except:
                raise ParsingError("Cannot parse command '%s'" % command)

        next_step = ''

        # We have 3 strings for each line of the canonical pattern

        add_step = ''
        del_step = ''
        clone_step = ''

        # Added is the list of elements we will add at to our environment
        # at the end of the step, we add them at the end so they are not
        # taken into account in the current step

        added = []
        cloned = []

        # If a node is in clone_wait, every cloning operation on it will
        # be delayed to next step. Same for other lists

        clone_wait = []
        merge_wait = []
        del_wait = []
        ad_wait = []

        # If we can't add a node with name n in this step, we don't want
        # another node with the same name to be added before it

        protected_names = []

        # For each action we update our lists and we chose what to do

        for i in range(len(actions)):
            action = actions[i]
            if action["keyword"] == "add_node":
                if action["node"] not in protected_names:
                    add_step += command_strings[i] + "\n"
                    added.append(action["node"])
            elif action["keyword"] == "delete_node":
                if action["node"] in env_nodes and\
                   action["node"] not in del_wait:
                    del_step += command_strings[i] + "\n"
                    env_nodes.remove(action["node"])
                else:
                    next_step += command_strings[i] + "\n"
                    ad_wait.append(action["node"])
            elif action["keyword"] == "add_node_attrs":
                if action["node"] in env_nodes and\
                   action["node"] not in ad_wait:
                    add_step += command_strings[i] + "\n"
                    added.append(action["node"])
                    clone_wait.append(action["node"])
                else:
                    next_step += command_strings[i] + "\n"
                    ad_wait.append(action["node"])
                    clone_wait.append(action["node"])
            elif action["keyword"] == "delete_node_attrs":
                if action["node"] in env_nodes and\
                   action["node"] not in del_wait:
                    del_step += command_strings[i] + "\n"
                else:
                    next_step += command_strings[i] + "\n"
                    clone_wait.append(action["node"])
                    ad_wait.append(action["node"])
            elif action["keyword"] == "add_edge":
                e = (action["node_1"], action["node_2"])
                if e[0] in env_nodes and\
                   e[1] in env_nodes and\
                   e[0] not in ad_wait and\
                   e[1] not in ad_wait:
                    add_step += command_strings[i] + "\n"
                    added.append(e)
                    if not di:
                        added.append((e[1], e[0]))
                    clone_wait.append(action["node_1"])
                    clone_wait.append(action["node_2"])
                else:
                    next_step += command_strings[i] + "\n"
                    clone_wait.append(action["node_1"])
                    clone_wait.append(action["node_2"])
                    merge_wait.append(action["node_1"])
                    merge_wait.append(action["node_2"])
            elif action["keyword"] == "delete_edge":
                e = (action["node_1"], action["node_2"])
                if (e in env_edges or
                    (not di and (e[1], e[0]) in env_edges)) and\
                   e[0] not in del_wait and\
                   e[1] not in del_wait:
                    is_cloned = False
                    for l in cloned:
                        if e[0] in l:
                            next_step += command_strings[i] + "\n"
                            clone_wait.append(action["node_1"])
                            clone_wait.append(action["node_2"])
                            merge_wait.append(action["node_1"])
                            merge_wait.append(action["node_2"])
                            is_cloned = True
                            break
                    if not is_cloned:
                        del_step += command_strings[i] + "\n"
                        clone_wait.append(action["node_1"])
                        clone_wait.append(action["node_2"])
                        env_edges.remove(e)
                        if not di:
                            env_edges.remove((e[1], e[0]))
                else:
                    next_step += command_strings[i] + "\n"
                    clone_wait.append(action["node_1"])
                    clone_wait.append(action["node_2"])
                    merge_wait.append(action["node_1"])
                    merge_wait.append(action["node_2"])
            elif action["keyword"] == "add_edge_attrs":
                e = (action["node_1"], action["node_2"])
                if (e in env_edges or
                    (not di and (e[1], e[0]) in env_edges)) and\
                   e[0] not in ad_wait and\
                   e[1] not in ad_wait:
                    add_step += command_strings[i] + "\n"
                    added.append(e)
                    if not di:
                        added.append((e[1], e[0]))
                    clone_wait.append(action["node_1"])
                    clone_wait.append(action["node_2"])
                else:
                    next_step += command_strings[i] + "\n"
                    clone_wait.append(action["node_1"])
                    clone_wait.append(action["node_2"])
                    merge_wait.append(action["node_1"])
                    merge_wait.append(action["node_2"])
            elif action["keyword"] == "delete_edge_attrs":
                e = (action["node_1"], action["node_2"])
                if (e in env_edges or
                    (not di and (e[1], e[0]) in env_edges)) and\
                   e[0] not in del_wait and\
                   e[1] not in del_wait:
                    is_cloned = False
                    for l in cloned:
                        if e[0] in l:
                            next_step += command_strings[i] + "\n"
                            clone_wait.append(action["node_1"])
                            clone_wait.append(action["node_2"])
                            merge_wait.append(action["node_1"])
                            merge_wait.append(action["node_2"])
                            is_cloned = True
                        elif e[1] in l:
                            next_step += command_strings[i] + "\n"
                            clone_wait.append(action["node_1"])
                            clone_wait.append(action["node_2"])
                            merge_wait.append(action["node_1"])
                            merge_wait.append(action["node_2"])
                            is_cloned = True
                    if not is_cloned:
                        del_step += command_strings[i] + "\n"
                        clone_wait.append(action["node_1"])
                        clone_wait.append(action["node_2"])
                else:
                    next_step += command_strings[i] + "\n"
                    clone_wait.append(action["node_1"])
                    clone_wait.append(action["node_2"])
                    merge_wait.append(action["node_1"])
                    merge_wait.append(action["node_2"])
            elif action["keyword"] == "clone":
                node = action["node"]
                if "node_name" in action.keys():
                    new_node = action["node_name"]
                else:
                    j = 1
                    new_node = str(node) + str(j)
                    while new_node in env_nodes or new_node in added:
                        j += 1
                        new_node = str(node) + str(j)
                if node in env_nodes and\
                   node not in clone_wait and\
                   new_node not in protected_names and\
                   fold_left(lambda e, acc: (e != node or
                                             (type(e) == tuple and
                                              e[1] != node and
                                                 e[0] != node)) and
                             acc,
                             True,
                             added):
                    clone_step += command_strings[i] + "\n"
                    added.append(new_node)
                    del_wait.append(node)
                    found = False
                    for i in range(len(cloned)):
                        if node in cloned[i]:
                            cloned[i].append(new_node)
                            found = True
                    if not found:
                        cloned.append([new_node, node])
                    to_add = []
                    for e in env_edges:
                        if e[0] == node:
                            to_add.append((new_node, e[1]))
                        elif e[1] == node:
                            to_add.append((e[0], new_node))
                    for e in added:
                        if type(e) == tuple:
                            if e[0] == node and\
                               e[1] != node:
                                to_add.append((new_node, e[1]))
                            elif e[1] == node and e[0] != node:
                                to_add.append((e[0], new_node))
                    for e in to_add:
                        added.append(e)
                else:
                    next_step += command_strings[i] + "\n"
                    del_wait.append(node)
                    merge_wait.append(node)
                    ad_wait.append(node)
                    protected_names.append(new_node)
            elif action["keyword"] == "merge":
                if "node_name" in actions[i].keys():
                    node_name = actions[i]["node_name"]
                else:
                    node_name = "_".join(actions[i]["nodes"])
                if fold_left(lambda n, acc: (n in env_nodes and
                                             n not in merge_wait) and
                             acc,
                             True,
                             action["nodes"]) and\
                        node_name not in protected_names:
                    add_step += command_strings[i] + "\n"

                    added.append(node_name)
                    clone_wait.append(node_name)

                    rem_el = []
                    for e in env_edges:
                        if e[0] in action["nodes"] and\
                           e[1] in action["nodes"]:
                            if e not in rem_el:
                                rem_el.append(e)
                        if e[0] in action["nodes"]:
                            if e not in rem_el:
                                rem_el.append(e)
                            if e[1] not in action["nodes"]:
                                added.append((node_name, e[1]))
                        elif e[1] in action["nodes"]:
                            if e not in rem_el:
                                rem_el.append(e)
                            if e[0] not in action["nodes"]:
                                added.append((e[0], node_name))
                    for e in rem_el:
                        while e in env_edges:
                            env_edges.remove(e)
                            if not di:
                                env_edges.remove((e[1], e[0]))
                    rem_el = []
                    for e in added:
                        if type(e) == tuple:
                            if e[0] in action["nodes"] and\
                               e[1] in action["nodes"]:
                                if e not in rem_el:
                                    rem_el.append(e)
                            if e[0] in action["nodes"]:
                                if e not in rem_el:
                                    rem_el.append(e)
                                if e[1] not in action["nodes"]:
                                    added.append((node_name, e[1]))
                            elif e[1] in action["nodes"]:
                                if e not in rem_el:
                                    rem_el.append(e)
                                if e[0] not in action["nodes"]:
                                    added.append((e[0], node_name))
                    for e in rem_el:
                        while e in added:
                            added.remove(e)
                            if not di:
                                added.remove((e[1], e[0]))
                else:
                    next_step += command_strings[i] + "\n"
                    protected_names.append(node_name)

        for el in added:
            if type(el) == tuple:
                env_edges.append(el)
            else:
                env_nodes.append(el)

        if len(next_step) != 0 and len(del_step + clone_step + add_step) == 0:
            raise ReGraphError(
                "Cannot find any new transformations and" +
                "the sequence of actions is non-empty : {}".format(next_step)
            )

        res.append(del_step + clone_step + add_step)

    return res


def assert_nx_graph_eq(g1, g2):
    """Assertion function for graph equality."""
    assert(set(g1.nodes()) == set(g2.nodes()))
    assert(set(g1.edges()) == set(g2.edges()))
    for n in g1.nodes():
        assert(g1.node[n] == g2.node[n])
    for e1, e2 in g1.edges():
        assert(g1.adj[e1][e2] == g2.adj[e1][e2])
    return


def format_typing(typing):
    if typing is None:
        typing = dict()
    new_typing = dict()
    for key, value in typing.items():
        if type(value) == dict:
            new_typing[key] = copy.deepcopy(value)
        else:
            try:
                if len(value) == 2:
                    new_typing[key] = copy.deepcopy(value)
                elif len(value) == 1:
                    new_typing[key] = copy.deepcopy(value[0])
            except:
                raise ReGraphError("Typing format is not valid!")
    return new_typing


def normalize_typing_relation(typing_rel):
    new_typing_rel = format_typing(typing_rel)
    for g, typing_rel in new_typing_rel.items():
        for key, values in typing_rel.items():
            value_set = set()
            if type(values) == str:
                value_set.add(values)
            else:
                try:
                    for v in values:
                        value_set.add(v)
                except TypeError:
                    value_set.add(values)
            if len(value_set) > 0:
                new_typing_rel[g][key] = value_set
    return new_typing_rel


def replace_source(n1, n2, mapping):
    mapping[n2] = mapping[n1]
    del mapping[n1]


def replace_target(n1, n2, mapping):
    for (key, value) in mapping.items():
        if value == n1:
            mapping[key] = n2


def id_of(elements):
    return {e: e for e in elements}


def restrict_mapping(nodes, mapping):
    new_mapping = {}
    for node in nodes:
        new_mapping[node] = mapping[node]
    return new_mapping


def reverse_image(mapping, nodes):
    return [node for node in mapping if mapping[node] in nodes]


def union_mappings(map1, map2):
    new_mapping = copy.deepcopy(map1)
    for (source, target) in map2.items():
        if source in new_mapping:
            if new_mapping[source] != target:
                raise ReGraphError("merging uncompatible mappings")
        else:
            new_mapping[source] = target
    return new_mapping


def recursive_merge(dict1, dict2):
    for k, v in dict2.items():
        if (k in dict1.keys() and
                isinstance(dict1[k], dict) and
                isinstance(v, dict)):
            recursive_merge(dict1[k], v)
        else:
            dict1[k] = v


def remove_forbidden(string):
            return string.replace(" ", "_").replace(
                "-", "_").replace(",", "_").replace(
                "/", "_").replace(".", "_")


def test_strictness(hierarchy, origin_id, rule, instance, p_typing, rhs_typing):
    """Test strictness of rewriting in a hierarchy."""
    ancestors = hierarchy.get_ancestors(origin_id).keys()
    for anc in ancestors:
        typing = hierarchy.get_typing(anc, origin_id)

        for lhs_n in rule.removed_nodes():
            graph_node = instance[lhs_n]
            anc_nodes = keys_by_value(typing, graph_node)
            if len(anc_nodes) > 0:
                raise RewritingError(
                    "Rewriting is strict (no propagation of removals is "
                    "allowed), the removed node '{}' from '{}' ".format(
                        graph_node, origin_id) +
                    "has instances '{}' in '{}'".format(
                        anc_nodes, anc))

        if len(rule.cloned_nodes()) > 0:
            for lhs_node, p_nodes in rule.cloned_nodes().items():
                graph_node = instance[lhs_node]
                anc_nodes = keys_by_value(typing, graph_node)
                if len(anc_nodes) > 0:
                    if anc not in p_typing:
                        raise RewritingError(
                            "Rewriting is strict (no propagation of clones is "
                            "allowed), the cloned node '{}' in '{}' ".format(
                                graph_node, origin_id) +
                            "has instances '{}' in '{}' and ".format(
                                anc_nodes, anc) +
                            "their typing by P is not specified")
                    else:
                        for anc_node in anc_nodes:
                            if anc_node not in p_typing[anc] or\
                                    len(p_typing[anc][anc_node]) != 1:
                                raise RewritingError(
                                    "Rewriting is strict (no propagation of clones is "
                                    "allowed), typing by a clone in P of the "
                                    "node '{}' in '{}' is required".format(
                                        anc_nodes, anc))

        anc_graph = hierarchy.get_graph(anc)

        for p_s, p_t in rule.removed_edges():
            graph_s = instance[rule.p_lhs[p_s]]
            graph_t = instance[rule.p_rhs[p_t]]
            anc_ss = keys_by_value(typing, graph_s)
            anc_ts = keys_by_value(typing, graph_t)
            for anc_s in anc_ss:
                for anc_t in anc_ts:
                    if anc_graph.exists_edge(anc_s, anc_t):
                        raise RewritingError(
                            "Rewriting is strict (no propagation of removals is "
                            "allowed), the removed edge '{}->{}' from '{}' ".format(
                                graph_s, graph_t, origin_id) +
                            "has an instance ('{}->{}') in '{}'".format(
                                anc_s, anc_t, anc))

        for lhs_node, attrs in rule.removed_node_attrs().items():
            graph_node = instance[lhs_node]
            anc_nodes = keys_by_value(typing, graph_node)
            for anc_node in anc_nodes:
                if valid_attributes(attrs, anc_graph.get_node(anc_node)):
                    raise RewritingError(
                        "Rewriting is strict (no propagation of removals is "
                        "allowed), the removed attributes '{}' from '{}' in '{}' ".format(
                            attrs, graph_node, origin_id) +
                        "have instances in '{}' from '{}'".format(
                            anc_node, anc))

        for p_s, p_t, attrs in rule.removed_edge_attrs():
            graph_s = instance[rule.p_lhs[p_s]]
            graph_t = instance[rule.p_rhs[p_t]]
            anc_ss = keys_by_value(typing, graph_s)
            anc_ts = keys_by_value(typing, graph_t)
            for anc_s in anc_ss:
                for anc_t in anc_ts:
                    if anc_graph.exists_edge(anc_s, anc_t):
                        if valid_attributes(
                                attrs, anc_graph.get_edge(anc_s, anc_t)):
                            raise RewritingError(
                                "Rewriting is strict (no propagation of removals is "
                                "allowed), the removed edge attributes '{}' ".format(
                                    attrs) +
                                "from '{}->{}' in '{}' ".format(
                                    graph_s, graph_t, origin_id) +
                                "have instances in '{}->{}' from '{}'".format(
                                    anc_s, anc_t, anc))

    descendants = hierarchy.get_descendants(origin_id).keys()
    for desc in descendants:
        typing = hierarchy.get_typing(origin_id, desc)

        for rhs_node, p_nodes in rule.merged_nodes().items():
            lhs_nodes = [rule.p_lhs[n] for n in p_nodes]
            graph_nodes = [instance[n] for n in lhs_nodes]
            types = set([
                typing[n]
                for n in graph_nodes
            ])
            if len(types) > 1:
                raise RewritingError(
                    "Rewriting is strict (no merging of types is "
                    "allowed), merged nodes '{}' from '{}' ".format(
                        graph_nodes, origin_id) +
                    "induces merging of '{}' from '{}'".format(
                        types, desc))

        if len(rule.added_nodes()) > 0:
            if desc not in rhs_typing:
                raise RewritingError(
                    "Rewriting is strict (no propagation of types is "
                    "allowed), typing of the added nodes '{}' ".format(
                        rule.added_nodes()) +
                    "by '{}' is required".format(desc))
            else:
                for rhs_n in rule.added_nodes():
                    if rhs_n not in rhs_typing[desc] or\
                            len(rhs_typing[desc][rhs_n]) != 1:
                        raise RewritingError(
                            "Rewriting is strict (no propagation of "
                            "types is allowed), typing of the added "
                            "node '{}' by '{}' is required".format(
                                rhs_n, desc))

        desc_graph = hierarchy.get_graph(desc)

        for rhs_node, attrs in rule.added_node_attrs().items():
            if rhs_node in rule.added_nodes():
                desc_node = list(rhs_typing[desc][rhs_node])[0]
                if not valid_attributes(attrs, desc_graph.get_node(desc_node)):
                    raise RewritingError(
                        "Rewriting is strict (no propagation of attribute "
                        "addition allowed), rule adds new attributes '{}' ".format(
                            attrs) +
                        "to the node '{}' from '{}'".format(desc_node, desc))
            else:
                lhs_nodes = [
                    rule.p_lhs[n]
                    for n in keys_by_value(rule.p_rhs, rhs_node)
                ]
                graph_nodes = [instance[n] for n in lhs_nodes]
                # There is only one type, otherwise it would fail before
                desc_node = [
                    typing[n]
                    for n in graph_nodes
                ][0]

                if not valid_attributes(attrs, desc_graph.get_node(desc_node)):
                    raise RewritingError(
                        "Rewriting is strict (no propagation of attribute "
                        "addition is allowed), rule adds new attributes "
                        "'{}' ".format(attrs) +
                        "to the node '{}' from '{}'".format(desc_node, desc))

        for rhs_s, rhs_t in rule.added_edges():

            if rhs_s in rule.added_nodes():
                desc_s = list(rhs_typing[desc][rhs_s])[0]
            else:
                lhs_nodes = [
                    rule.p_lhs[n]
                    for n in keys_by_value(rule.p_rhs, rhs_s)
                ]
                graph_nodes = [instance[n] for n in lhs_nodes]

                # There is only one type, otherwise it would fail before
                desc_s = [
                    typing[n]
                    for n in graph_nodes
                ][0]

            if rhs_t in rule.added_nodes():
                desc_t = list(rhs_typing[desc][rhs_t])[0]
            else:
                lhs_nodes = [
                    rule.p_lhs[n]
                    for n in keys_by_value(rule.p_rhs, rhs_t)
                ]
                graph_nodes = [instance[n] for n in lhs_nodes]

                # There is only one type, otherwise it would fail before
                desc_t = [
                    typing[n]
                    for n in graph_nodes
                ][0]

            if not desc_graph.exists_edge(desc_s, desc_t):
                raise RewritingError(
                    "Rewriting is strict (no propagation of edge "
                    "addition is allowed), rule adds new edge "
                    "'{}->{}' ".format(desc_s, desc_t) +
                    "in '{}'".format(desc))

        for rhs_s, rhs_t, attrs in rule.added_edge_attrs().items():
            if rhs_s in rule.added_nodes():
                desc_s = list(rhs_typing[desc][rhs_s])[0]
            else:
                lhs_nodes = [
                    rule.p_lhs[n]
                    for n in keys_by_value(rule.p_rhs, rhs_s)
                ]
                graph_nodes = [instance[n] for n in lhs_nodes]

                # There is only one type, otherwise it would fail before
                desc_s = [
                    typing[n]
                    for n in graph_nodes
                ][0]

            if rhs_t in rule.added_nodes():
                desc_t = list(rhs_typing[desc][rhs_t])[0]
            else:
                lhs_nodes = [
                    rule.p_lhs[n]
                    for n in keys_by_value(rule.p_rhs, rhs_t)
                ]
                graph_nodes = [instance[n] for n in lhs_nodes]

                # There is only one type, otherwise it would fail before
                desc_t = [
                    typing[n]
                    for n in graph_nodes
                ][0]
            desc_attrs = desc_graph.get_edge(desc_s, desc_t)
            if not valid_attributes(attrs, desc_attrs):
                raise RewritingError(
                    "Rewriting is strict (no propagation of attribute "
                    "addition is allowed), rule adds new attributes "
                    "'{}' ".format(attrs) +
                    "to the edge '{}->{}' from '{}'".format(desc_s, desc_t, desc))
