//
// Created by Paras Sharma on 6/7/2020.
//

#include "Tree.h"
#include <math.h>
#include <algorithm>
#include <iostream>
#include <random>
#include <fstream>
#include <set>
#include <time.h>

Tree::Tree(Canvas *canvas_, float threshold_theta_, float resolution_angle_, float step_size_){
//    Canvas *canvas1 = canvas;
    canvas = canvas_;
    threshold_theta = threshold_theta_;
    resolution_angle = resolution_angle_;
    step_size = step_size_;
    nodes.push_back(canvas_->start.first);
    special_nodes.push_back(canvas_->start.first);
//    gauss1 = new Gaussian(5., 10.f, 0.5);
//    gauss2 = new Gaussian(std::fmod(-5., 360.), 10.f,0.5);
    gauss1 = new Gaussian(10., 10.f, 0.5, 0);
    gauss2 = new Gaussian(-10, 10.f,0.5, 0);
    //gauss1 = new Gaussian(10., 10.f, 0.25, 90*M_PI/180);
    //gauss2 = new Gaussian(-10, 10.f,0.25, 90*M_PI/180);
    std::vector<Gaussian> gauss_;
    gauss_.emplace_back(*gauss1); gauss_.emplace_back(*gauss2);
//    GMM start_gmm(gauss_, true);
    prob_dist[canvas_->start.first].gauss_list = gauss_;
    parent[canvas_->start.first] =  canvas_->start.first;
    std::set<std::pair<Node, float>> se{std::pair(canvas_->start.first, canvas_->start.second)};
    parents[std::pair(canvas_->start.first, canvas_->start.second)] = se;
//    setup_action(canvas_->start);
    std::vector<float> v{canvas_->start.second};
    actions[canvas_->start.first] = v;
    actions_taken[canvas_->start.first] = true;
    std::set<float> s{canvas_->start.second};
    available_yaws[canvas_->start.first] = s;
    std::set<float> s1;
    rejected_yaws[canvas_->start.first] = s1;
}

//void Tree::setup_action(Node node) {
//    std::vector<std::pair<float, Node>> action;
//    Node sample = Utils::extend(node, canvas->end, step_size);
//    for(int angle=0; angle<ceil(360/resolution_angle); angle++){
//        Node sample_location = Utils::rotate(node, sample, angle*resolution_angle);
//        bool flag = false;
//        for(auto &node_:actions_taken){
//            if(Utils::eul_dist(node_.first, sample_location) < step_size/(pow(2, .5))){
//                flag = true;
//                break;
//            }
//        }
//        if(!flag){
//            actions_taken[sample_location] = true;
//            action.emplace_back(std::pair(angle*resolution_angle, sample_location));
//        }
//    }
//    if(!action.empty()){
//        actions[node] = action;
//    } else {
////        std::ofstream myfile;
////        myfile.open ("removed.txt", std::ios_base::app);
////        myfile << std::get<0>(node) << " " << std::get<1>(node) <<"\n";
////        myfile.close();
//    }
//}

bool Tree::check_threshold(Node node, Node parent_, float yaw){
    float temp = INFINITY;
//    if(parents.find(std::pair(parent_, yaw)) == parents.end()){
////        std::cout << "BA";
//    }
    for(auto parent__: parents[std::pair(parent_, yaw)]){
        if(temp>std::min(Utils::get_angle(node, parent_, std::get<0>(parent__)), std::abs(360 - Utils::get_angle(node, parent_, std::get<0>(parent__))))){
            temp = std::min(Utils::get_angle(node, parent_, std::get<0>(parent__)), std::abs(360 - Utils::get_angle(node, parent_, std::get<0>(parent__))));
        }
    }
    return temp > 180 - threshold_theta;
}


bool Tree::add_node(Node parent_, Node node, float yaw, Gaussian *gauss){
    bool collision_free = true; //AG: This is to indicate if node addition is successful
    if(!canvas->check_collision(node, parent_, step_size)){
        bool flag = true;
        for (auto node_: nodes){
            bool plot_flag = true;
            //AG: This is to reduce the node clutter & finiding is there exist another node in the vicinity
            if(Utils::eul_dist(node_, node) < step_size/pow(2,.5)){
                for(int angle=0; angle<ceil(360/resolution_angle); angle++){
                    //AG: Checking kinematic constraint on the selected node
                    if (Utils::feasible(parent_, yaw, node_, angle*resolution_angle, MAX_STEER_ANGLE)){
                        if(rejected_yaws[node_].find(angle*resolution_angle)==rejected_yaws[node_].end()) {
                            if(available_yaws[node_].find(angle*resolution_angle)==available_yaws[node_].end()) {
                                available_yaws[node_].insert(angle * resolution_angle);
                                if (actions.find(node_) == actions.end()) {
                                    std::vector<float> v;
                                    actions[node_] = v;
                                }
                                if (std::find(actions[node_].begin(), actions[node_].end(), angle * resolution_angle) ==
                                    actions[node_].end()) {
                                    actions[node_].emplace_back(angle * resolution_angle);
                                    if (std::find(special_nodes.begin(), special_nodes.end(), node_) ==
                                        special_nodes.end()) {
                                        special_nodes.emplace_back(node_);

                                    }
                                }
                            }
                        }
                        if (parents.find(std::pair(node_, angle*resolution_angle)) == parents.end()) {
                            std::set<std::pair<Node, float>> s;
                            parents[std::pair(node_, angle*resolution_angle)] = s;
                        }
                        parents[std::pair(node_, angle*resolution_angle)].insert(std::pair(parent_, yaw));
                        if (plot_flag && print_file) {
                            std::ofstream myfile;
                            myfile.open("kino.txt", std::ios_base::app);
                            myfile << std::get<0>(node_) << " " << std::get<1>(node_) << " "
                                   << std::get<0>(parent_) << " " << std::get<1>(parent_) << "\n";
                            myfile.close();
                            plot_flag = false;
                        }
                    }
                }
                flag = false;
                collision_free = false;
            }
        }
        if(flag){ //AG: Creating a new Node
            nodes.emplace_back(node);
            parent[node] = parent_;
            std::vector<float> v;
            actions[node] = v;
            std::set<float> s;
            available_yaws[node] = s;
            std::set<float> s1;
            rejected_yaws[node] = s1;
            for(int angle=0; angle<ceil(360/resolution_angle); angle++){
                //AG: Store all the possbile <node, action> pairs for the given <parent, yaw> combination
                //AG: actions and available_yaw stores all the possible actions for the new node from <parent, yaw> pair
                if (Utils::feasible(parent_, yaw, node, angle*resolution_angle, MAX_STEER_ANGLE)){
                    //TODO: This if can be removed as the new node is just created
                    if(available_yaws[node].find(angle*resolution_angle)==available_yaws[node].end()){
                        available_yaws[node].insert(angle*resolution_angle);
                        if(actions.find(node)==actions.end()){
                            std::vector<float> v;
                            actions[node] = v;
                        }
                        if(parents.find(std::pair(node, angle*resolution_angle))==parents.end()){
                            std::set<std::pair<Node, float>> s;
                            parents[std::pair(node, angle*resolution_angle)] = s;
                        }
                        parents[std::pair(node, angle*resolution_angle)].insert(std::pair(parent_, yaw));
                        if (std::find(actions[node].begin(), actions[node].end(),angle*resolution_angle)==actions[node].end()){
                            actions[node].emplace_back(angle*resolution_angle);
                        }
                    }
                }
            }


            prob_dist[node] = prob_dist[parent_]; //Look for pointer issue
            //AG: Copy the Gaussian from parent and update all the Gaussian for child
            for(auto &gauss_ : prob_dist[node].gauss_list){
                float mean_shift = resolution_angle * 0.2;
                float variance_shift = 2;
                gauss_.mean = Utils::shift_toward(gauss_.mean, 0, mean_shift);
                gauss_.variance -= variance_shift;
                gauss_.variance = std::max(5.f, gauss_.variance);
            }

            special_nodes.push_back(node);
            bool fake = true;
            //AG: Check for Special Node. check_threshold returns true if the parent is not special
            if(parent[parent_]!=parent_ && check_threshold(node, parent_, yaw)){
                fake = false;
                if (std::find(special_nodes.begin(), special_nodes.end(),parent_)!=special_nodes.end()){
                    special_nodes.erase(std::remove(special_nodes.begin(), special_nodes.end(), parent_), special_nodes.end());
                }
            }
//            if(fake){
//                std::cout << "NA";
//            }
        }
    } else{
        collision_free = false;
    }
    // TODO: migrate change_probability to GMM class
    //AG: Update the probabitlity of Parent node
    change_proability(reinterpret_cast<Gaussian *>(&gauss));

    return collision_free;
}

//AG: return value: is_sucessfull, node, yaw_direction
std::tuple<bool, Node, float> Tree::make_action(Node node, std::pair<float , Gaussian> sampled_direction){
    if(actions.find(node) != actions.end()){
        std::vector<float> actions_ = actions[node];
        if(actions_.empty()){
            actions.erase(node);
            // TODO:: change this
            return std::tuple(false, std::make_tuple(-1, -1, -1), -1);
        }
        float closest = actions_[0];
        for(auto action: actions_){
            if(Utils::dist_mean(action, sampled_direction.first) < Utils::dist_mean(closest, sampled_direction.first)){
                closest = action;
            }
        }
        Node sample = Utils::extend(node, canvas->end.first, step_size);
        sample = Utils::rotate(node, sample, closest, sampled_direction.second.axis, step_size);
        remove_action(node, closest);
        rejected_yaws[node].insert(closest);
        return std::make_tuple(true, sample, closest);
    }
    // TODO:: change this
    return std::make_tuple(false, std::make_tuple(-1, -1, -1), -1);
}

//AG: Remove the action from the current node which is used to generate a new sample
//Remove the node from special node list if all the actions are exhausted
void Tree::remove_action(Node node, float action) {
    std::vector<float> actions_ = actions[node];
    // TODO: Remove nested loop
    if (std::find(actions_.begin(), actions_.end(),action)!=actions_.end()){
        actions[node].erase(std::remove(actions[node].begin(), actions[node].end(), action), actions[node].end());
    }
    if(actions[node].empty()){
//        std::ofstream myfile;
//        myfile.open ("removed.txt", std::ios_base::app);
//        myfile << std::get<0>(node) << " " << std::get<1>(node) <<"\n";
//        myfile.close();
        actions.erase(node);
        prev_special_nodes.emplace_back(node);
        special_nodes.erase(std::remove(special_nodes.begin(), special_nodes.end(), node), special_nodes.end());
        used_special_nodes[node] = true;
    }
}

void Tree::get_path(Node end_node) {
    struct Node_{
        std::pair<Node, float> node_;
        std::pair<Node, float> parent_;
        std::vector<std::pair<Node, float>> childs;
    };
    std::vector<std::pair<Node, float>> queue;
    std::map<std::pair<Node, float>, Node_> nodes_;
    for(int angle=0; angle<ceil(360/resolution_angle); angle++) {
        if(parents.find(std::pair(end_node, angle*resolution_angle))!=parents.end()){
            queue.emplace_back(std::pair(end_node, angle*resolution_angle));
            Node_ n;
            n.node_ = std::pair(end_node, angle*resolution_angle);
            n.parent_ = std::pair(end_node, angle*resolution_angle);
            nodes_[std::pair(end_node, angle*resolution_angle)] = n;
        }
    }
    std::pair<Node, float> current;
    std::map<std::pair<Node, float>, bool> visited;
    while(true){
        current = queue.front();
        queue.erase(queue.begin());
        if(current==canvas->start){
            break;
        }
        if(visited.find(current)!=visited.end()){
            continue;
        }
        visited[current] = true;
        std::copy(parents[current].begin(), parents[current].end(), std::back_inserter(nodes_[current].childs));
        for(auto parent__: nodes_[current].childs){
            if(visited.find(parent__)==visited.end()){
                Node_ n;
                n.node_ = parent__;
                n.parent_ = current;
                nodes_[parent__] = n;
                queue.emplace_back(parent__);
                std::ofstream myfile;
                myfile.open ("removed.txt", std::ios_base::app);
                myfile << std::get<0>(parent__.first) << " " << std::get<1>(parent__.first) <<"\n";
                myfile.close();
            }
        }
    }
    std::vector<std::pair<Node, float>> path;
    while (current.first!=end_node){
        path.emplace_back(current);
        if(print_file){
            std::ofstream myfile;
            myfile.open ("path.txt", std::ios_base::app);
            myfile << std::get<0>(current.first) << " " << std::get<1>(current.first) <<"\n";
            myfile.close();
        }
        current = nodes_[current].parent_;
    }
    std::cout<<path.size()<<std::endl;
}

//AG: return: parent_node_, new_node_, direction_, parent_gaussian_  
std::tuple<Node, Node, float, Gaussian> Tree::pick_random(int &iterations) {
    std::default_random_engine generator;
    generator.seed(time(0));
    while(true){
        iterations++;
        if(special_nodes.empty()){
            std::set<Node> special_nodes_;
            for(auto node: prev_special_nodes){
                bool  flag1 = false;
                //AG: This is to pick the parent(parent(parent(node))) till we find a node which was not used as a special node earlier
                while (used_special_nodes.find(node)!=used_special_nodes.end()){
                    node = parent[node];
                    flag1 = true;
                    if(node==canvas->start.first){
                        break;
                    }
                }
                if (node!=canvas->start.first){
                    if(flag1) {
                        special_nodes_.insert(node);
                    }else {
                        special_nodes_.insert(parent[node]);
                    }
                }
            }
            if (special_nodes_.empty()){
                std::cout << "NO PATH" << std::endl;
                std::exit(true);
            }
            prev_special_nodes.clear();
            std::copy(special_nodes_.begin(), special_nodes_.end(), std::back_inserter(special_nodes));
        }
        std::uniform_real_distribution<> dis(0, special_nodes.size()-1);
        int random_index = ceil(dis(generator));
        Node parent_ = special_nodes[random_index];
        std::pair<float , Gaussian> sample_direction = prob_dist[parent_].sample();
        std::tuple<bool, Node, float> new_Node = make_action(parent_, sample_direction);
        if(std::get<0>(new_Node)){
            return std::make_tuple(parent_, std::get<1>(new_Node), std::get<2>(new_Node), sample_direction.second);
        } else{
            if(actions[parent_].empty()) {
                prev_special_nodes.emplace_back(parent_);
                special_nodes.erase(std::remove(special_nodes.begin(), special_nodes.end(), parent_),
                                    special_nodes.end());
            }
        }
    }
}

void Tree::change_proability(Gaussian *gaussian) {
    float mean_shift = resolution_angle*.9f;
    gaussian->mean = Utils::shift_away(gaussian->mean,  0, mean_shift);
    float variance_shift = 2.f;
    gaussian->variance += variance_shift;
    gaussian->variance = fmax(5, gaussian->variance);
}
