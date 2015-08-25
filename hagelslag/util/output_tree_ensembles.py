import cPickle
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input scikit-learn tree ensemble model pickle file.")
    parser.add_argument("-o", "--output", help="Output file.")
    args = parser.parse_args()
    tree_ensemble_obj = load_tree_object(args.input)
    output_tree_ensemble(tree_ensemble_obj, args.output)
    return


def load_tree_object(filename):
    with open(filename) as file_obj:
        tree_ensemble_obj = cPickle.load(file_obj)
    return tree_ensemble_obj


def output_tree_ensemble(tree_ensemble_obj, output_filename, attribute_names=None):
    out_file = open(output_filename, "w")
    for t, tree in enumerate(tree_ensemble_obj.estimators_):
        out_file.write("Tree {0:d}\n".format(t))
        tree_str = print_tree_recursive(tree.tree_, 0, attribute_names)
        out_file.write(tree_str)
        out_file.write("\n")
    out_file.close()
    return


def print_tree_recursive(tree_obj, node_index, attribute_names=None):
    tree_str = ""
    if node_index == 0:
        tree_str += "{0:d}\n".format(tree_obj.node_count)
    if tree_obj.feature[node_index] >= 0:
        if attribute_names is None:
            attr_val = "{0:d}".format(tree_obj.feature[node_index])
        else:
            attr_val = attribute_names[tree_obj.feature[node_index]]
        tree_str += "b {0:d} {1} {2:0.4f} {3:d} {4:0.2f}\n".format(node_index,
                                                                   attr_val,
                                                                   tree_obj.weighted_n_node_samples[node_index],
                                                                   tree_obj.n_node_samples[node_index],
                                                                   tree_obj.threshold[node_index])
    else:
        if tree_obj.max_n_classes > 1:
            leaf_value = "{0:d}".format(tree_obj.value[node_index].argmax())
        else:
            leaf_value = "{0:0.4f}".format(tree_obj.value[node_index])
        tree_str += "l {0:d} {1} {2:0.4f} {3:d}\n".format(node_index,
                                                          leaf_value,
                                                          tree_obj.weighted_n_node_samples[node_index],
                                                          tree_obj.n_node_samples[node_index])
    if tree_obj.children_left[node_index] > 0:
        tree_str += print_tree_recursive(tree_obj, tree_obj.children_left[node_index], attribute_names)
    if tree_obj.children_right[node_index] > 0:
        tree_str += print_tree_recursive(tree_obj, tree_obj.children_right[node_index], attribute_names)
    return tree_str

if __name__ == "__main__":
    main()