//
// Created by Paras Sharma on 6/7/2020.
//

#ifndef PGRRT_TREE_H
#define PGRRT_TREE_H

#include <vector>
#include <tuple>
#include <map>
#include <set>
#include "GMM.h"
#include "Canvas.h"
#include "config.h"
#define Node std::tuple<float, float>
class Tree {



public:
    Tree(Canvas *canvas, float threshold_theta, float resolution_angle, float step_size);

    std::tuple<std::tuple<float, float>, std::tuple<float, float>, float, Gaussian> pick_random(int &iterations);

    bool add_node(Node parent, Node node, float yaw, Gaussian *gaussian);
    bool check_threshold(Node node, Node parent, float yaw);

    Canvas *canvas;
    float step_size;
    std::vector <Node> nodes;
    std::vector <Node> special_nodes;         //AG: This will hold the current candidate nodes
    std::vector <Node> prev_special_nodes;    //AG: This will hold the nodes which were special in the last collection of special_nodes but now out of all the actions
    std::map <Node, bool> used_special_nodes; //AG: This will list all the nodes which were special nodes at some time but now exausted
    std::map <Node, GMM> prob_dist;
    std::map <Node, Node> parent;
    std::map <std::pair<Node, float>, std::set<std::pair<Node, float>>> parents; //AG: This will save the <current node and action> and all the various <parent and yaw> pairs used to reach this combination
    std::map <Node, std::vector<float>> actions; //AG: This will hold the nodes on which action has been taken and the list of actions
    std::map <Node, bool> actions_taken;
    std::map<Node, std::set<float>> available_yaws;
    std::map<Node, std::set<float>> rejected_yaws;
    float threshold_theta;
    float resolution_angle;
    Gaussian *gauss1;
    Gaussian *gauss2;

//    void setup_action(Node node);

    std::tuple<bool, std::tuple<float, float>, float> make_action(Node node, float sampled_direction);

    void remove_action(Node node, float  action);

    void change_proability(Gaussian *gaussian);

    void get_path(Node end_node);
};


#endif //PGRRT_TREE_H
