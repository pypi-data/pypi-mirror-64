"""Collection of utils for generation of propagation-related Cypher queries."""
import networkx as nx
import warnings

from regraph.exceptions import (TypingWarning, InvalidHomomorphism)
from regraph.utils import (keys_by_value,
                           generate_new_id,
                           attrs_intersection,
                           attrs_union)
from regraph.primitives import (add_nodes_from,
                                add_edges_from,
                                get_edge,
                                get_node,
                                print_graph,
                                exists_edge)
from regraph.networkx.category_utils import (pullback,
                                             pushout,
                                             image_factorization,
                                             compose)
from regraph.rules import Rule

from . import generic
from . import rewriting


# def check_functional()

def get_typing(domain, codomain, typing_label, attrs=None):
    query = (
        "MATCH (n:{})-[:{}]-(m:{})\n".format(
            domain, typing_label, codomain) +
        "RETURN n.id as node, m.id as type"
    )
    return query


def set_intergraph_edge(domain, codomain, domain_node,
                        codomain_node, typing_label,
                        attrs=None):
    query = (
        "MATCH (n:{} {{ id: '{}' }}), (m:{} {{ id: '{}' }})\n".format(
            domain, domain_node, codomain, codomain_node) +
        "MERGE (n)-[:{}  {{ {} }}]->(m)".format(typing_label, generic.generate_attributes(attrs))
    )
    return query


def check_homomorphism(tx, domain, codomain, total=True):
    """Check if the homomorphism is valid.

    Parameters
    ----------
    tx
        Variable of a cypher transaction
    domain : str
        Label of the graph at the domain of the homomorphism
    codmain : str
        Label of the graph at the codomain of the homomorphism

    Raises
    ------
    InvalidHomomorphism
        This error is raised in the following cases:

            * a node at the domain does not have exactly 1 image
            in the codoamin
            * an edge at the domain does not have an image in
            the codomain
            * a property does not match between a node and its image
            * a property does not match between an edge and its image
    """
    # Check if all the nodes of the domain have exactly 1 image
    query1 = (
        "MATCH (n:{})\n".format(domain) +
        "OPTIONAL MATCH (n)-[:typing]->(m:{})\n".format(codomain) +
        "WITH n, collect(m) as images\n" +
        "WHERE size(images) <> 1\n" +
        "RETURN n.id as ids, size(images) as nb_of_img\n"
    )

    result = tx.run(query1)
    nodes = []

    for record in result:
        nodes.append((record['ids'], record['nb_of_img']))
    if len(nodes) != 0:
        raise InvalidHomomorphism(
            "Wrong number of images!\n" +
            "\n".join(
                ["The node '{}' of the graph {} have {} image(s) in the graph {}.".format(
                    n, domain, str(nb), codomain) for n, nb in nodes]))

    # Check if all the edges of the domain have an image
    query2 = (
        "MATCH (n:{})-[:edge]->(m:{})\n".format(
            domain, domain) +
        "MATCH (n)-[:typing]->(x:{}), (y:{})<-[:typing]-(m)\n".format(
            codomain, codomain) +
        "OPTIONAL MATCH (x)-[r:edge]->(y)\n" +
        "WITH x.id as x_id, y.id as y_id, r\n" +
        "WHERE r IS NULL\n" +
        "WITH x_id, y_id, collect(r) as rs\n" +
        "RETURN x_id, y_id\n"
    )

    result = tx.run(query2)
    xy_ids = []
    for record in result:
        xy_ids.append((record['x_id'], record['y_id']))
    if len(xy_ids) != 0:
        raise InvalidHomomorphism(
            "Edges are not preserved in the homomorphism from '{}' to '{}': ".format(
                domain, codomain) +
            "Was expecting edges {}".format(
                ", ".join(
                    "'{}'->'{}'".format(x, y) for x, y in xy_ids))
        )

    # "CASE WHEN size(apoc.text.regexGroups(m_props, 'IntegerSet\\[(\\d+|minf)-(\\d+|inf)\\]') AS value"

    # Check if all the attributes of a node of the domain are in its image
    query3 = (
        "MATCH (n:{})-[:typing]->(m:{})\n".format(
            domain, codomain) +
        "WITH properties(n) as n_props, properties(m) as m_props, " +
        "n.id as n_id, m.id as m_id\n" +
        "WITH REDUCE(invalid = 0, k in filter(k in keys(n_props) WHERE k <> 'id' AND k <> 'count') |\n" +
        "\tinvalid + CASE\n" +
        "\t\tWHEN NOT k IN keys(m_props) THEN 1\n" +
        "\t\tELSE REDUCE(invalid_values = 0, v in n_props[k] |\n" +
        "\t\t\tinvalid_values + CASE m_props[k]\n" +
        "\t\t\t\tWHEN ['IntegerSet'] THEN CASE WHEN toInt(v) IS NULL THEN 1 ELSE 0 END\n" +
        "\t\t\t\tWHEN ['StringSet'] THEN CASE WHEN toString(v) <> v THEN 1 ELSE 0 END\n" +
        "\t\t\t\tWHEN ['BooleanSet'] THEN CASE WHEN v=true OR v=false THEN 0 ELSE 1 END\n" +
        "\t\t\t\tELSE CASE WHEN NOT v IN m_props[k] THEN 1 ELSE 0 END END)\n" +
        "\t\tEND) AS invalid, n_id, m_id\n" +
        "WHERE invalid <> 0\n" +
        "RETURN n_id, m_id, invalid\n"
    )

    result = tx.run(query3)
    invalid_typings = []
    for record in result:
        invalid_typings.append((record['n_id'], record['m_id']))
    if len(invalid_typings) != 0:
        raise InvalidHomomorphism(
            "Node attributes are not preserved in the homomorphism from '{}' to '{}': ".format(
                domain, codomain) +
            "\n".join(["Attributes of nodes source: '{}' ".format(n) +
                       "and target: '{}' do not match!".format(m)
                       for n, m in invalid_typings]))

    # Check if all the attributes of an edge of the domain are in its image
    query4 = (
        "MATCH (n:{})-[rel_orig:edge]->(m:{})\n".format(
            domain, domain) +
        "MATCH (n)-[:typing]->(x:{}), (y:{})<-[:typing]-(m)\n".format(
            codomain, codomain) +
        "MATCH (x)-[rel_img:edge]->(y)\n" +
        "WITH n.id as n_id, m.id as m_id, x.id as x_id, y.id as y_id, " +
        "properties(rel_orig) as rel_orig_props, " +
        "properties(rel_img) as rel_img_props\n" +
        "WITH REDUCE(invalid = 0, k in keys(rel_orig_props) |\n" +
        "\tinvalid + CASE\n" +
        "\t\tWHEN NOT k IN keys(rel_img_props) THEN 1\n" +
        "\t\tELSE REDUCE(invalid_values = 0, v in rel_orig_props[k] |\n" +
        "\t\t\tinvalid_values + CASE rel_img_props[k]\n" +
        "\t\t\t\tWHEN ['IntegerSet'] THEN CASE WHEN toInt(v) IS NULL THEN 1 ELSE 0 END\n" +
        "\t\t\t\tWHEN ['StringSet'] THEN CASE WHEN toString(v) <> v THEN 1 ELSE 0 END\n" +
        "\t\t\t\tWHEN ['BooleanSet'] THEN CASE WHEN v=true OR v=false THEN 0 ELSE 1 END\n" +
        "\t\t\t\tELSE CASE WHEN NOT v IN rel_img_props[k] THEN 1 ELSE 0 END END)\n" +
        "\t\tEND) AS invalid, n_id, m_id, x_id, y_id\n" +
        "WHERE invalid <> 0\n" +
        "RETURN n_id, m_id, x_id, y_id, invalid\n"
    )
    result = tx.run(query4)
    invalid_edges = []
    for record in result:
        invalid_edges.append((record['n_id'], record['m_id'],
                              record['x_id'], record['y_id']))
    if len(invalid_edges) != 0:
        raise InvalidHomomorphism(
            "Edge attributes are not preserved!\n" +
            "\n".join(["Attributes of edges '{}'->'{}' ".format(n, m) +
                       "and '{}'->'{}' do not match!".format(x, y)
                       for n, m, x, y in invalid_edges])
        )

    return True


def check_consistency(tx, source, target):
    """Check if the adding of a homomorphism is consistent."""
    query = (
        "// match all typing pairs between '{}' and '{}'\n".format(
            source, target) +
        "MATCH (s:{})-[:typing]->(t:{})\n".format(
            source, target) +
        "WITH s, t\n"
    )
    query += (
        "// match all the predecessors of 's' and successors of 't'\n"
        "MATCH (pred)-[:typing*0..]->(s), (t)-[:typing*0..]->(suc) \n"
        "WHERE NOT pred = s AND NOT suc = t\n" +
        "WITH s, t, collect(DISTINCT pred) as pred_list, " +
        "collect(DISTINCT suc) as suc_list\n"
    )
    query += (
        "// select all the pairs 'pred' 'suc' with a path between\n"
        "UNWIND pred_list as pred\n" +
        "UNWIND suc_list as suc\n" +
        "OPTIONAL MATCH (pred)-[r:typing*]->(suc)\n" +
        "WHERE NONE(rel in r WHERE rel.tmp = 'True')\n"
        "WITH s, t, r, labels(pred)[1] as pred_label, labels(suc)[1] as suc_label\n" +
        "WHERE r IS NOT NULL\n" +
        "WITH DISTINCT s, t, pred_label, suc_label\n"
    )
    query += (
        "// return the pairs 's' 't' where there should be a typing edge\n"
        "OPTIONAL MATCH (s)-[new_typing:typing]->(t)\n" +
        "WHERE new_typing.tmp IS NOT NULL\n" +
        "WITH pred_label, suc_label, s.id as s_id, t.id as t_id, new_typing\n" +
        "WHERE new_typing IS NULL\n" +
        "RETURN pred_label, suc_label, s_id, t_id\n"
    )
    result = tx.run(query)

    missing_typing = []
    for record in result:
        missing_typing.append((record['pred_label'], record['suc_label']))
    if len(missing_typing) != 0:
        raise InvalidHomomorphism(
            "Homomorphism does not commute with existing paths:\n" +
            ",\n".join(["\t- from {} to {}".format(
                s, t) for s, t in missing_typing]) + "."
        )

    return True


def check_consistency_with_rm(tx, source, target, typing_label):
    """Check consistency of typing after removeal of tagged nodes."""
    consistent = True

    query = (
        "MATCH (G:{})\n".format(source) +
        "WHERE G.id = '{}'\n".format(source) +
        "OPTIONAL MATCH (h_i:{})\n".format(target) +
        "WHERE (G)<-[:{}*1..]-(h_i})-[:{}*1..]->(G)\n".format(
            typing_label, typing_label)
    )


def check_tmp_consistency(tx, source, target, typing_label):
    """Check consistency of typing of the rhs of the rule."""
    query1 = (
        "// Checking consistency of introduced rhs\n"
        "MATCH (G:{})\n".format(source) +
        "WHERE G.id = '{}'\n".format(source) +
        "OPTIONAL MATCH (t_i:{})\n".format(target) +
        "WHERE (t_i)<-[:{}*1..]-(G)-[:{}*1..]->(t_i)\n".format(
            typing_label, typing_label) +
        "WITH DISTINCT t_i\n" +
        "RETURN collect(t_i.id)\n"
    )

    # If graph doesn't have multiple paths to the same successorts
    # then there is nothing to check
    multiple_paths_successors = tx.run(query1).value()[0]
    if len(multiple_paths_successors) == 0:
        return True

    inconsistent_paths = []
    for graph in multiple_paths_successors:
        query2 = (
            "MATCH (n:{})-[:tmp_typing]->()-[:typing*0..]->(m:{})\n".format(
                source, graph) +
            "WITH n, collect(DISTINCT m.id) as imgs\n" +
            "WHERE size(imgs) > 1\n" +
            "RETURN n.id as n_id, imgs\n"
        )
        result = tx.run(query2)
        for record in result:
            inconsistent_paths.append((record['n_id'], record['imgs'], graph))

    if len(inconsistent_paths) == 0:
        return True

    else:
        warn_message = (
            "\nTyping of the rhs is self inconsistent:\n" +
            "\n".join(["\t- Node '{}' is typed as {} in {}".format(
                n,
                " and ".join(["'{}'".format(i) for i in imgs]),
                g) for n, imgs, g in inconsistent_paths]) +
            "\n\n" +
            "The rhs typing of the rule will be ignored and a canonical " +
            "rewriting will be performed!\n"
        )
        warnings.warn(warn_message, TypingWarning)
        return False


def propagate_clones(tx, graph_id, predecessor_id):
    # query_n = (
    #     "// Matching of the nodes to clone in '{}'\n".format(predecessor_id) +
    #     "OPTIONAL MATCH (node_to_clone:{})-[t:typing]->(n:{})\n".format(
    #         predecessor_id, graph_id) +
    #     "WITH node_to_clone, collect(n) as sucs, collect(t) as typ_sucs, "
    #     "count(n) as number_of_img\n" +
    #     "WHERE number_of_img >= 2 AND node_to_clone IS NOT NULL\n" +
    #     "RETURN node_to_clone, number_of_img - 1 as number_of_clones"
    # )
    # result = tx.run(query_n)
    # clone_count = dict()
    # for record in result:
    #     clone_count[record['node_to_clone']['id']] =\
    #         record['number_of_clones']

    query_n = (
        "// Matching of the nodes to clone in '{}'\n".format(predecessor_id) +
        "OPTIONAL MATCH (node_to_clone:{})-[t:typing]->(n:{})\n".format(
            predecessor_id, graph_id) +
        "WITH collect(n) as clones, count(n) as n_img, node_to_clone\n" +
        "WHERE n_img > 1 AND node_to_clone IS NOT NULL\n" +
        "RETURN node_to_clone, clones\n"
    )
    result = tx.run(query_n)
    clones = dict()
    for record in result:
        clones[record['node_to_clone']['id']] =\
            [c["id"] for c in record['clones']]

    # get interclone edges
    query_interclone_edges = (
        "OPTIONAL MATCH (tn:{})<-[:typing]-(n:{})-[r:edge]->(m:{})-[:typing]->(tm:{}), \n".format(
            graph_id, predecessor_id, predecessor_id, graph_id) +
        "(tn)-[tr:edge]->(tm)\n" +
        "WHERE n.id IN [{}] AND m.id IN [{}] AND tr IS NOT NULL\n".format(
            ", ".join(["'{}'".format(k) for k in clones.keys()]),
            ", ".join(["'{}'".format(k) for k in clones.keys()])) +
        "RETURN tn.id as u, tm.id as v, properties(r) as attrs\n"
    )
    result = tx.run(query_interclone_edges)
    interclone_edges = dict()

    for record in result:
        interclone_edges[record["u"], record["v"]] =\
            generic.properties_to_attributes([record], "attrs")

    fixed_nodes = dict()
    clone_results = dict()
    for original, graph_clones in clones.items():
        clone_results[original] = dict()
        for i, c in enumerate(graph_clones):
            if i == 0:
                fixed_nodes[original] = c
                clone_results[original] = c
            else:
                query = (
                    generic.match_node(
                        'x', original,
                        node_label=predecessor_id) +
                    rewriting.cloning_query(
                        original_var='x',
                        clone_var='new_node',
                        clone_id_var='uid',
                        clone_id="clone_" + original,
                        node_label=predecessor_id,
                        edge_labels=["edge", "relation"],
                        ignore_naming=True)[0] +
                    "OPTIONAL MATCH (x)-[t:typing]-(m:{} {{id: '{}'}})\n".format(
                        graph_id, c) +
                    "DELETE t\n" +
                    "MERGE (new_node)-[:typing]->(m)\n" +
                    generic.return_vars(['uid'])
                )
                result = tx.run(query)
                uid_records = []
                for record in result:
                    uid_records.append(record['uid'])
                if len(uid_records) > 0:
                    clone_id = uid_records[0]
                    clone_results[clone_id] = c

    # add interclone edges
    visited_edges = set()
    for n, tn in clone_results.items():
        for m, tm in clone_results.items():
            if (tn, tm) in interclone_edges.keys() and\
               (n, m) not in visited_edges:
                visited_edges.add((n, m))
                query = generic.match_nodes(
                    {"n_" + n: n, "n_" + m: m},
                    node_label=predecessor_id)
                query += rewriting.add_edge(
                    edge_var='new_edge',
                    source_var="n_" + n,
                    target_var="n_" + m,
                    edge_label="edge",
                    attrs=interclone_edges[(tn, tm)],
                    merge=True)
                tx.run(query)


def clone_propagation_query(graph_id, predecessor_id):
    """Generate query for propagation of cloning to a predecessor graph."""
    # We clone the nodes that have more than 1 image and
    # reassign the typing edges
    carry_vars = set()
    query = (
        "// Matching of the nodes to clone in '{}'\n".format(predecessor_id) +
        "OPTIONAL MATCH (node_to_clone:{})-[t:typing]->(n:{})\n".format(
            predecessor_id, graph_id) +
        "WITH node_to_clone, collect(n) as sucs, collect(t) as typ_sucs, "
        "count(n) as number_of_img\n" +
        "WHERE number_of_img >= 2 AND node_to_clone IS NOT NULL\n"
    )
    query += (
        "FOREACH(t IN typ_sucs | DELETE t)\n" +
        "WITH node_to_clone, sucs, number_of_img-1 as number_of_clone\n"
    )
    carry_vars.update(['node_to_clone', 'sucs'])
    query += (
        rewriting.multiple_cloning_query(
            original_var='node_to_clone',
            clone_var='cloned_node',
            clone_id='clone_id',
            clone_id_var='clone_id',
            number_of_clone_var='number_of_clone',
            node_label=predecessor_id,
            edge_label='edge',
            preserv_typing=True,
            carry_vars=carry_vars,
            ignore_naming=True,
            multiple_rows=True)[0]
    )
    carry_vars.difference_update(['cloned_node', 'clone_id'])
    query += (
        "WITH collect(cloned_node)+[node_to_clone] as nodes_to_typ, " +
        "collect(clone_id) as clone_ids, " +
        ", ".join(carry_vars) + "\n" +
        "FOREACH (i IN range(0, size(sucs)-1) |\n" +
        "\tFOREACH(source in [nodes_to_typ[i]] |\n"
        "\t\tFOREACH(target in [sucs[i]] |\n"
        "\t\t\t" + rewriting.add_edge(
            edge_var='restored_typing',
            source_var='source',
            target_var='target',
            edge_label='typing') + ")))\n"
    )
    query += "RETURN clone_ids"
    return query


def remove_node_propagation_query(graph_id, predecessor_id):
    """Generate query for propagation of node deletes to a predecessor."""
    # Removes nodes and node attrs
    carry_vars = set()
    query = (
        "// Removal of nodes in '{}'\n".format(predecessor_id) +
        "MATCH (n:{})\n".format(predecessor_id) +
        "OPTIONAL MATCH (n)-[:typing]->(x:{})\n".format(graph_id) +
        "FOREACH(dummy IN CASE WHEN x IS NULL THEN [1] ELSE [] END |\n" +
        "\t" + rewriting.remove_nodes(['n']) + ")\n"
        "// Removal of node attributes in '{}'\n".format(predecessor_id) +
        "WITH n, x\n".format(
            predecessor_id, graph_id) +
        "WHERE x IS NOT NULL AND " +
        generic.nb_of_attrs_mismatch('n', 'x') + " <> 0\n"
        "WITH n, x, [x, n] as node_to_merge_props\n"
    )
    carry_vars.update(['n', 'x'])
    query += (
        generic.merge_properties_from_list(
            list_var='node_to_merge_props',
            new_props_var='new_props',
            carry_vars=carry_vars,
            method='intersection') +
        "WITH n.id as n_id, " + ", ".join(carry_vars) + "\n"
        "SET n = new_props\n" +
        "SET n.id = n_id\n"
    )
    return query


def remove_edge_propagation_query(graph_id, predecessor_id):
    """Generate query for propagation of edge deletes to a predecessor."""
    carry_vars = set()
    query = (
        "// Removal of edges attributes in '{}'\n".format(predecessor_id) +
        "MATCH (n:{})-[rel_pred:edge]->(m:{})\n".format(
            predecessor_id, predecessor_id) +
        "OPTIONAL MATCH (x:{})-[rel:edge]->(y:{})".format(
            graph_id, graph_id) +
        "WHERE (n)-[:typing]->(x) AND (m)-[:typing]->(y)\n" +
        "FOREACH(dummy IN CASE WHEN rel IS NULL THEN [1] ELSE [] END |\n" +
        "\t" + rewriting.remove_edge('rel_pred') + ")\n" +
        "WITH rel, rel_pred\n" +
        "WHERE rel IS NOT NULL AND " +
        generic.nb_of_attrs_mismatch('rel_pred', 'rel') + " <> 0\n"
        "WITH rel, rel_pred, [rel_pred, rel] as edges_to_merge_props\n"
    )
    carry_vars.update(['rel_pred', 'rel'])
    query += (
        generic.merge_properties_from_list(
            list_var='edges_to_merge_props',
            new_props_var='new_props',
            carry_vars=carry_vars,
            method='intersection') +
        "SET rel_pred = new_props\n"
    )
    return query


def merge_propagation_query(graph_id, successor_id):
    """Generate query for propagation of merges to a successor graph."""
    carry_vars = set()
    carry_vars.add('merged_nodes')
    query = "\n// Up-propagation to the graph '{}'\n".format(successor_id)
    query += (
        "\n// Matching of the nodes to merge in '{}'\n".format(successor_id) +
        "WITH [] as merged_nodes\n"
        "OPTIONAL MATCH (n:{})-[r:typing]->(node_to_merge:{})\n".format(
            graph_id, successor_id) +
        "WITH n, collect(DISTINCT r) as rels, collect(DISTINCT node_to_merge) as nodes_to_merge, " +
        ", ".join(carry_vars) + "\n"
        "FOREACH(dummy IN CASE WHEN size(rels) > 1 AND size(nodes_to_merge) = 1 THEN [null] ELSE [] END |\n" +
        "\t FOREACH(rel IN rels | DELETE rel)\n" +
        "\t FOREACH(m in nodes_to_merge |\n" +
        "\t CREATE (n)-[:typing]->(m)))\n" +
        "WITH n, nodes_to_merge, merged_nodes\n" +
        "WHERE n IS NOT NULL AND size(nodes_to_merge) >= 2\n"
    )
    carry_vars.add('n')
    carry_vars.add('nodes_to_merge')
    query += (
        rewriting.merging_from_list(
            list_var='nodes_to_merge',
            merged_var='merged_node',
            merged_id='id',
            merged_id_var='merged_id',
            node_label=successor_id,
            edge_label='edge',
            merge_typing=True,
            carry_vars=carry_vars,
            ignore_naming=True,
            multiple_rows=True,
            multiple_var='n')[0]
    )
    carry_vars.remove('merged_node')
    carry_vars.remove('merged_id')
    query += "RETURN collect(merged_id) as merged_nodes"
    return query


# def add_propa

def propagate_add_node(tx, origin_graph_id, graph_id, successor_id):
    carry_vars = set()
    query = (
        "// Add new nodes if needed to {}\n".format(successor_id) +
        "MATCH (n:{}) WHERE NOT (n)-[:typing]->(:{}) \n".format(
            graph_id, successor_id) +
        "// Match existing image of some predecessor that commutes\n" +
        "OPTIONAL MATCH (n)<-[:typing*1..]-(pred)-[:typing*1..]->(existing_img:{})\n".format(
            successor_id) +
        "FOREACH(dummy IN CASE WHEN existing_img IS NOT NULL THEN [1] ELSE [] END |\n" +
        "\tMERGE (n)-[:typing]->(existing_img))\n" +
        generic.with_vars(['n']) +
        "OPTIONAL MATCH (n)<-[:typing*]-" +
        "(:{})-[trans_type:transitive_typing]->(successor_node:{})\n".format(
            origin_graph_id, successor_id) +
        "\tFOREACH(dummy IN CASE WHEN trans_type IS NULL THEN [] ELSE [1] END |\n" +
        "\t\tMERGE (n)-[:typing]->(successor_node)\n" +
        "\t\tDELETE trans_type)\n"
    )
    tx.run(query)

    query = (
        "MATCH (n:{}) WHERE NOT (n)-[:typing]->(:{})\n".format(
            graph_id, successor_id) +
        "MERGE (n)-[:typing]->(node_img:{})\n".format(successor_id) +
        "WITH n, node_img\n" +
        "FOREACH(dummy IN CASE WHEN node_img.id IS NULL THEN [1] ELSE [] END |\n" +
        "\tSET node_img.id = toString(id(node_img)))\n"
    )
    tx.run(query)

    query = (
        "MATCH (n:{})-[:typing]->(m:{})\n".format(graph_id, successor_id) +
        "WITH n, m WHERE " + generic.nb_of_attrs_mismatch('n', 'm') + " <> 0\n" +
        "WITH m, collect(n) + [m] as nodes_to_merge_props\n"
    )

    carry_vars.add('m')
    query += (
        generic.merge_properties_from_list(
            list_var='nodes_to_merge_props',
            new_props_var='new_props',
            carry_vars=carry_vars,
            method='union') +
        "SET m += new_props\n"
    )
    # print(query)
    tx.run(query)
    return query
# def add_node_propagation_query(tx, origin_graph_id, graph_id, successor_id):
#     """Generate query for propagation of node adds to a successor graph.."""
#     carry_vars = set()
#     # add nodes in T for each node without image in G + add new_props
#     query = (
#         "// Addition of nodes and attributes in '{}'\n".format(
#             successor_id) +
#         "MATCH (n:{})\n".format(graph_id) +
#         "OPTIONAL MATCH (n)<-[:typing*0..]-(pred)-[:typing*0]->(existing_img:{})\n".format(
#             successor_id) +
#         "WHERE NOT pred = n AND NOT pred = existing_img\n" +
#         "FOREACH(dummy IN CASE WHEN existing_img IS NOT NULL THEN [1] ELSE [] END |\n" +
#         "\tMERGE (n)-[:typing]->(existing_img))\n" +
#         generic.with_vars(['n']) +
#         "OPTIONAL MATCH (n)<-[:typing*]-" +
#         "(:{})-[trans_type:transitive_typing]->(existing_img:{})\n".format(
#             origin_graph_id, successor_id) +
#         "\tFOREACH(dummy IN CASE WHEN trans_type IS NULL THEN [] ELSE [1] END |\n" +
#         "\t\tMERGE (n)-[:typing]->(existing_img)\n" +
#         "\t\tDELETE trans_type)\n" +
#         generic.with_vars(['n'])
#     )
#     tx.run(query)

#     query = (
#         "MERGE (n)-[:typing]->(node_img:{})\n".format(successor_id) +
#         "WITH n, node_img\n" +
#         "FOREACH(dummy IN CASE WHEN node_img.id IS NULL THEN [1] ELSE [] END |\n" +
#         "\tSET node_img.id = toString(id(node_img)))\n" +
#         "WITH n, node_img WHERE " +
#         generic.nb_of_attrs_mismatch('n', 'node_img') + " <> 0\n" +
#         "WITH node_img, collect(n) + [node_img] as nodes_to_merge_props\n"
#     )
#     carry_vars.add('node_img')
#     query += (
#         generic.merge_properties_from_list(
#             list_var='nodes_to_merge_props',
#             new_props_var='new_props',
#             carry_vars=carry_vars,
#             method='union') +
#         "SET node_img += new_props\n"
#     )
#     tx.run(query)
#     return query


def propagate_add_edge(tx, graph_id, successor_id):
    carry_vars = set()

    query = (
        "// Match existing edges with attribute mismatch\n" +
        "MATCH (tn:{})<-[:typing]-(n:{})-[r:edge]->(m:{})-[:typing]->(tm:{}),\n".format(
            successor_id, graph_id, graph_id, successor_id) +
        "\t(tn)-[tr:edge]->(tm)\n" +
        "WITH tn, tm, r, tr WHERE " +
        generic.nb_of_attrs_mismatch('r', 'tr') + " <> 0\n"
        "WITH tn, tm, tr, collect(r) + [tr] as edges_to_merge_props\n"
    )
    carry_vars.add("tr")
    query += (
        generic.merge_properties_from_list(
            list_var='edges_to_merge_props',
            new_props_var='new_props',
            carry_vars=carry_vars,
            method='union') +
        "SET tr += new_props\n"
    )
    tx.run(query)
    query = (
        "// Add new edges to {}\n".format(successor_id) +
        "MATCH (tn:{})<-[:typing]-(n:{})-[r:edge]->(m:{})-[:typing]->(tm:{})\n".format(
            successor_id, graph_id, graph_id, successor_id) +
        "WHERE NOT (tn)-[:edge]->(tm) \n".format(
            graph_id, successor_id) +
        "CREATE (tn)-[tr:edge]->(tm)\n" +
        "SET tr = r\n"
    )
    tx.run(query)
    query = (
        "// Add missing loops to {}\n".format(successor_id) +
        "MATCH (tn:{})<-[:typing]-(n:{})-[r:edge]->(m:{})\n".format(
            successor_id, graph_id, graph_id) +
        "WHERE n=m AND NOT (tn)-[:edge]->(tn)\n" +
        "CREATE (tn)-[tr:edge]->(tn)\n" +
        "SET tr = r\n"
    )
    tx.run(query)

    return query


def add_edge_propagation_query(graph_id, successor_id):
    """Generate query for propagation of edge adds to a successor graph."""
    carry_vars = set()
    # add edges in T for each edge without image in G + add new_props
    query = (
        "\n// Addition of edges and attributes in '{}'\n".format(
            successor_id) +
        "MATCH (n:{})-[rel:edge]->(m:{}), ".format(
            graph_id, graph_id) +
        "(n)-[:typing]->(x:{}), (m)-[:typing]->(y:{})\n".format(
            successor_id, successor_id) +
        "MERGE (x)-[rel_img:edge]->(y)\n" +
        "WITH x, y, rel, rel_img WHERE " +
        generic.nb_of_attrs_mismatch('rel', 'rel_img') + " <> 0\n"
        "WITH x, y, rel_img, collect(rel) + rel_img as edges_to_merge_props\n"
    )
    carry_vars.update(['x', 'y', 'rel_img'])
    query += (
        generic.merge_properties_from_list(
            list_var='edges_to_merge_props',
            new_props_var='new_props',
            carry_vars=carry_vars,
            method='union') +
        "SET rel_img += new_props\n"
    )
    return query


def remove_targeted_typing(rewritten_graph):
    query = (
        "MATCH (m:{})<-[r:_to_remove]-(n)-[path:typing*1..]->(m)\n".format(rewritten_graph) +
        # "WHERE m.id = o.id\n" +
        "DELETE r\n" +
        "FOREACH(rel IN path |\n" +
        "\tDELETE rel)\n"
    )
    return query


def remove_targetting(rewritten_graph):
    query = (
        "MATCH ()-[rel:_to_remove]->(:{})\n".format(rewritten_graph) +
        "DELETE rel\n"

    )
    return query


def remove_tmp_typing(rewritten_graph, direction="successors"):
    if direction == "predecessors":
        left_arrow = "<"
        right_arrow = ""
    else:
        left_arrow = ""
        right_arrow = ">"
    query = (
        "Removing ':tmp_typing' relationships."
        "MATCH (n:{}){}-[t:tmp_typing]-{}()\n".format(
            rewritten_graph, left_arrow, right_arrow) +
        "DELETE t\n"
    )
    return query


def preserve_tmp_typing(rewritten_graph, graph_label, typing_label,
                        direction="successors"):
    if direction == "predecessors":
        left_arrow = "<"
        right_arrow = ""
    else:
        left_arrow = ""
        right_arrow = ">"
    query = (
        "// Replacing ':tmp_typing' with ':typing'\n"
        "MATCH (n:{}){}-[t:tmp_typing]-{}(m)\n".format(
            rewritten_graph, left_arrow, right_arrow) +
        "OPTIONAL MATCH (:{} {{id: '{}'}})".format(
            graph_label, rewritten_graph) +
        "{}-[skeleton_rel:{}]-{}(:{} {{id: labels(m)[0]}}) \n".format(
            left_arrow, typing_label, right_arrow, graph_label) +
        "FOREACH( dummy IN (CASE skeleton_rel WHEN null THEN [] ELSE [1] END) | \n" +
        "\tDELETE t\n" +
        "\tMERGE (n){}-[:typing]-{}(m)\n".format(left_arrow, right_arrow) +
        ")\n" +
        "FOREACH( dummy IN (CASE skeleton_rel WHEN null THEN [1] ELSE [] END) | \n" +
        "\tDELETE t\n" +
        "\tMERGE (n){}-[:transitive_typing]-{}(m)\n".format(
            left_arrow, right_arrow) +
        ")\n"
    )
    return query


def get_rule_liftings(tx, graph_id, rule, instance, p_typing=None):
    """Execute the query finding rule liftings."""
    if p_typing is None:
        p_typing = {}

    liftings = {}
    if len(rule.lhs.nodes()) > 0:
        lhs_vars = {
            n: n for n in rule.lhs.nodes()}
        match_instance_vars = {lhs_vars[k]: v for k, v in instance.items()}

        # Match nodes
        query = "// Match nodes the instance of the rewritten graph \n"
        query += "MATCH {}".format(
            ", ".join([
                "({}:{} {{id: '{}'}})".format(k, graph_id, v)
                for k, v in match_instance_vars.items()
            ])
        )
        query += "\n\n"

        carry_vars = list(lhs_vars.values())
        for k, v in lhs_vars.items():
            query += (
                "OPTIONAL MATCH (n)-[:typing*1..]->({})\n".format(v) +
                "WITH {} \n".format(
                    ", ".join(carry_vars + [
                        "collect({{type:'node', origin: {}.id, id: n.id, graph:labels(n)[0], attrs: properties(n)}}) as {}_dict\n".format(
                            v, v)])
                )
            )
            carry_vars.append("{}_dict".format(v))
        # Match edges
        for (u, v) in rule.lhs.edges():
            edge_var = "{}_{}".format(lhs_vars[u], lhs_vars[v])
            query += "OPTIONAL MATCH ({}_instance)-[{}:edge]->({}_instance)\n".format(
                lhs_vars[u],
                edge_var,
                lhs_vars[v])
            query += "WHERE ({})-[:typing*1..]->({}) AND ({})-[:typing*1..]->({})\n".format(
                "{}_instance".format(lhs_vars[u]), lhs_vars[u],
                "{}_instance".format(lhs_vars[v]), lhs_vars[v])
            query += (
                "WITH {} \n".format(
                    ", ".join(carry_vars + [
                        "collect({{type: 'edge', source: {}.id, target: {}.id, attrs: properties({}), graph:labels({})[0]}}) as {}\n".format(
                            "{}_instance".format(lhs_vars[u]),
                            "{}_instance".format(lhs_vars[v]),
                            edge_var,
                            "{}_instance".format(lhs_vars[u]),
                            edge_var)
                    ])
                )
            )
            carry_vars.append(edge_var)
        query += "RETURN {}".format(
            ", ".join(
                ["{}_dict as {}".format(v, v) for v in lhs_vars.values()] +
                ["{}_{}".format(lhs_vars[u], lhs_vars[v]) for u, v in rule.lhs.edges()]))

        result = tx.run(query)
        record = result.single()
        l_g_ls = {}
        lhs_nodes = {}
        lhs_edges = {}
        for k, v in record.items():
            if len(v) > 0:
                if v[0]["type"] == "node":
                    for el in v:
                        if el["graph"] not in lhs_nodes:
                            lhs_nodes[el["graph"]] = []
                            l_g_ls[el["graph"]] = {}
                        l_g_ls[el["graph"]][el["id"]] = keys_by_value(
                            instance, el["origin"])[0]
                        # compute attr intersection
                        attrs = attrs_intersection(
                            generic.convert_props_to_attrs(el["attrs"]),
                            get_node(rule.lhs, l_g_ls[el["graph"]][el["id"]]))
                        lhs_nodes[el["graph"]].append((el["id"], attrs))

                else:
                    for el in v:
                        if el["graph"] not in lhs_edges:
                            lhs_edges[el["graph"]] = []
                        # compute attr intersection
                        attrs = attrs_intersection(
                            generic.convert_props_to_attrs(el["attrs"]),
                            get_edge(
                                rule.lhs,
                                l_g_ls[el["graph"]][el["source"]],
                                l_g_ls[el["graph"]][el["target"]]))
                        lhs_edges[el["graph"]].append(
                            (el["source"], el["target"], attrs)
                        )

        for graph, nodes in lhs_nodes.items():

            lhs = nx.DiGraph()
            add_nodes_from(lhs, nodes)
            if graph in lhs_edges:
                add_edges_from(
                    lhs, lhs_edges[graph])

            p, p_lhs, p_g_p = pullback(
                lhs, rule.p, rule.lhs, l_g_ls[graph], rule.p_lhs)

            l_g_g = {n[0]: n[0] for n in nodes}

            # Remove controlled things from P_G
            if graph in p_typing.keys():
                l_g_factorization = {
                    keys_by_value(l_g_g, k)[0]: v
                    for k, v in p_typing[graph].items()
                }
                p_g_nodes_to_remove = set()
                for n in p.nodes():
                    l_g_node = p_lhs[n]
                    # If corresponding L_G node is specified in
                    # the controlling relation, remove all
                    # the instances of P nodes not mentioned
                    # in this relations
                    if l_g_node in l_g_factorization.keys():
                        p_nodes = l_g_factorization[l_g_node]
                        if p_g_p[n] not in p_nodes:
                            del p_g_p[n]
                            del p_lhs[n]
                            p_g_nodes_to_remove.add(n)

                for n in p_g_nodes_to_remove:
                    p.remove_node(n)

            liftings[graph] = {
                "rule": Rule(p=p, lhs=lhs, p_lhs=p_lhs),
                "instance": l_g_g,
                "l_g_l": l_g_ls[graph],
                "p_g_p": p_g_p
            }
    else:
        query = generic.ancestors_query(graph_id, "graph", "homomorphism")
        result = tx.run(query)
        ancestors = [record["ancestor"] for record in result]
        for a in ancestors:
            liftings[a] = {
                "rule": Rule.identity_rule(),
                "instance": {},
                "l_g_l": {},
                "p_g_p": {}
            }

    return liftings


def get_rule_projections(tx, hierarchy, graph_id, rule, instance, rhs_typing=None):
    """Execute the query finding rule liftings."""
    if rhs_typing is None:
        rhs_typing = {}

    projections = {}

    if rule.is_relaxing():
        if len(rule.lhs.nodes()) > 0:
            lhs_instance = {
                n: instance[n] for n in rule.lhs.nodes()
            }
            lhs_vars = {
                n: n for n in rule.lhs.nodes()}
            match_instance_vars = {
                v: lhs_instance[k] for k, v in lhs_vars.items()
            }

            # Match nodes
            query = "// Match nodes the instance of the rewritten graph \n"
            query += "MATCH {}".format(
                ", ".join([
                    "({}:{} {{id: '{}'}})".format(k, graph_id, v)
                    for k, v in match_instance_vars.items()
                ])
            )
            query += "\n\n"

            carry_vars = list(lhs_vars.values())
            for k, v in lhs_vars.items():
                query += (
                    "OPTIONAL MATCH (n)<-[:typing*1..]-({})\n".format(v) +
                    "WITH {} \n".format(
                        ", ".join(
                            carry_vars +
                            ["collect(DISTINCT {{type:'node', origin: {}.id, id: n.id, graph:labels(n)[0], attrs: properties(n)}}) as {}_dict\n".format(
                                v, v)])
                    )
                )
                carry_vars.append("{}_dict".format(v))

            # Match edges
            for (u, v) in rule.p.edges():
                edge_var = "{}_{}".format(lhs_vars[u], lhs_vars[v])
                query += "OPTIONAL MATCH ({}_instance)-[{}:edge]->({}_instance)\n".format(
                    lhs_vars[u],
                    edge_var,
                    lhs_vars[v])
                query += "WHERE ({})<-[:typing*1..]-({}) AND ({})<-[:typing*1..]-({})\n".format(
                    "{}_instance".format(lhs_vars[u]), lhs_vars[u],
                    "{}_instance".format(lhs_vars[v]), lhs_vars[v])
                query += (
                    "WITH {} \n".format(
                        ", ".join(carry_vars + [
                            "collect({{type: 'edge', source: {}.id, target: {}.id, graph:labels({})[0], attrs: properties({})}}) as {}\n".format(
                                "{}_instance".format(lhs_vars[u]),
                                "{}_instance".format(lhs_vars[v]),
                                "{}_instance".format(lhs_vars[u]),
                                edge_var,
                                edge_var)
                        ])
                    )
                )
                carry_vars.append(edge_var)
            query += "RETURN {}".format(
                ", ".join(
                    ["{}_dict as {}".format(v, v) for v in lhs_vars.values()] +
                    ["{}_{}".format(lhs_vars[u], lhs_vars[v]) for u, v in rule.p.edges()]))

            result = tx.run(query)
            record = result.single()

            l_l_ts = {}
            l_nodes = {}
            l_edges = {}
            for k, v in record.items():
                if len(v) > 0:
                    if v[0]["type"] == "node":
                        for el in v:
                            l_node = keys_by_value(instance, el["origin"])[0]
                            if el["graph"] not in l_nodes:
                                l_nodes[el["graph"]] = {}
                                l_l_ts[el["graph"]] = {}
                            if el["id"] not in l_nodes[el["graph"]]:
                                l_nodes[el["graph"]][el["id"]] = {}
                            l_nodes[el["graph"]][el["id"]] = attrs_union(
                                l_nodes[el["graph"]][el["id"]],
                                attrs_intersection(
                                    generic.convert_props_to_attrs(el["attrs"]),
                                    get_node(rule.lhs, l_node)))
                            l_l_ts[el["graph"]][l_node] = el["id"]
                    else:
                        for el in v:
                            l_sources = keys_by_value(l_l_ts[el["graph"]], el["source"])
                            l_targets = keys_by_value(l_l_ts[el["graph"]], el["target"])

                            for l_source in l_sources:
                                for l_target in l_targets:
                                    if exists_edge(rule.l, l_source, l_target):
                                        if el["graph"] not in l_edges:
                                            l_edges[el["graph"]] = {}
                                        if (el["source"], el["target"]) not in l_edges[el["graph"]]:
                                            l_edges[el["graph"]][(el["source"], el["target"])] = {}
                                        l_edges[el["graph"]][(el["source"], el["target"])] =\
                                            attrs_union(
                                                l_edges[el["graph"]][(el["source"], el["target"])],
                                                attrs_intersection(
                                                    generic.convert_props_to_attrs(el["attrs"]),
                                                    get_edge(rule.lhs, l_source, l_target)))

        for graph, typing in hierarchy.get_descendants(graph_id).items():
            if graph in l_nodes:
                nodes = l_nodes[graph]
            else:
                nodes = {}
            if graph in l_edges:
                edges = l_edges[graph]
            else:
                edges = {}

            l = nx.DiGraph()
            add_nodes_from(l, [(k, v) for k, v in nodes.items()])
            if graph in l_edges:
                add_edges_from(
                    l,
                    [(s, t, v) for (s, t), v in edges.items()])

            rhs, p_rhs, r_r_t = pushout(
                rule.p, l, rule.rhs, compose(rule.p_lhs, l_l_ts[graph]), rule.p_rhs)

            l_t_t = {n: n for n in nodes}

            # Modify P_T and R_T according to the controlling
            # relation rhs_typing
            if graph in rhs_typing.keys():
                r_t_factorization = {
                    r_r_t[k]: v
                    for k, v in rhs_typing[graph].items()
                }
                added_t_nodes = set()
                for n in rhs.nodes():
                    if n in r_t_factorization.keys():
                        # If corresponding R_T node is specified in
                        # the controlling relation add nodes of T
                        # that type it to P
                        t_nodes = r_t_factorization[n]
                        for t_node in t_nodes:
                            if t_node not in l_t_t.values() and\
                               t_node not in added_t_nodes:
                                new_p_node = generate_new_id(
                                    l.nodes(), t_node)
                                l.add_node(new_p_node)
                                added_t_nodes.add(t_node)
                                p_rhs[new_p_node] = n
                                l_t_t[new_p_node] = t_node
                            else:
                                p_rhs[keys_by_value(l_t_t, t_node)[0]] = n

            projections[graph] = {
                "rule": Rule(p=l, rhs=rhs, p_rhs=p_rhs),
                "instance": l_t_t,
                "l_l_t": l_l_ts[graph],
                "p_p_t": {k: l_l_ts[graph][v] for k, v in rule.p_lhs.items()},
                "r_r_t": r_r_t
            }

    return projections
