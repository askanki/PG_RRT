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
#include "Utils.h"

class Tree {


//Threshold_theta : SP Angle, Resolution Angle: For action space
public:
    Tree(Canvas *canvas, float threshold_theta, float resolution_angle, float step_size);

    std::tuple<Node, Node, float, Gaussian *> pick_random(int &iterations, std::default_random_engine *generator);

    std::pair<bool,bool> add_node(Node parent, Node node, float yaw, Gaussian *gaussian);
    bool check_threshold(Node node, Node parent, float yaw, float axis);

    Canvas *canvas;
    float step_size;
    std::vector <Node> nodes;
    std::vector <Node> special_nodes;         //AG: This will hold the current candidate nodes
    std::vector <Node> prev_special_nodes;    //AG: This will hold the nodes which were special in the last collection of special_nodes but now out of all the actions
    std::map <Node, bool> used_special_nodes; //AG: This will list all the nodes which were special nodes at some time but now exausted
    std::map <Node, GMM> prob_dist;           //AG: This will save the node and the associated GMM   
    std::map <Node, Node> parent;             //AG: This will store the current node and it's parent
    //std::tuple<Node, Yaw, Axis>
    //std::map <std::pair<Node, float>, std::set<std::pair<Node, float>>> parents; 
    std::map <std::tuple<Node, float, float>, std::set<std::tuple<Node, float, float>>> parents; //AG: This will save the <current node and feasible action> from all possible <parent and yaw> pairs used to reach this combination
    //std::map <Node, std::vector<float>> actions;  
    std::map <Node, Orientation> actions; //AG: This will hold the nodes on which action has been taken and the list of actions; This is used in make_action function and will on;y contain the available feasible actions which have not been taken yet 
    std::map <Node, bool> actions_taken;         //AG: This will indicate if an action is taken from a particular node  
    //std::map<Node, std::vector<float>> available_yaws; 
    //std::map<Node, std::vector<float>> rejected_yaws;
    std::map<Node, Orientation> available_yaws;  //AG: This will hold the nodes on which action has been taken and the list of all feasible actions;
    std::map<Node, Orientation> rejected_yaws;
    float threshold_theta;
    float resolution_angle;
    
    Gaussian *gauss1;
    Gaussian *gauss2;

//    void setup_action(Node node);

    std::tuple<bool, Node, float> make_action(Node node, std::pair<float , Gaussian *> sampled_direction);

    void remove_action(Node node, float  action, float axis);

    void change_proability(Gaussian *gaussian);

    void get_path(Node end_node);
};


#endif //PGRRT_TREE_H
