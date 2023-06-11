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
    //AG: Gaussian(mean, variance, probability, axis)
    gauss1 = new Gaussian(10., 10.f, 0.5, 0);
    gauss2 = new Gaussian(-10, 10.f,0.5, 0);
    //gauss1 = new Gaussian(10., 10.f, 0.25, 90*M_PI/180);
    //gauss2 = new Gaussian(-10, 10.f,0.25, 90*M_PI/180);
    std::vector<Gaussian> gauss_;
    gauss_.emplace_back(*gauss1); 
    gauss_.emplace_back(*gauss2);
    prob_dist[canvas_->start.first].gauss_list = gauss_;
    parent[canvas_->start.first] =  canvas_->start.first;
    //TODO: Fix the Axis of the starting and end node; it should be w.r.t. the some refrence frame
    std::set<std::tuple<Node, float, float>> se{std::tuple(canvas_->start.first, canvas_->start.second, 0.)};
    parents[std::tuple(canvas_->start.first, canvas_->start.second, 0.)] = se;
//    setup_action(canvas_->start);
    //std::vector<float> v{canvas_->start.second};
    Orientation v;
    v[0].push_back(canvas_->start.second);
    actions[canvas_->start.first] = v;
    actions_taken[canvas_->start.first] = true;
    //std::set<float> s{canvas_->start.second};
    Orientation s;
    s[0].push_back(canvas_->start.second);
    available_yaws[canvas_->start.first] = s;
    std::vector<float> s1;
    Orientation o1;
    o1[0] = s1;
    rejected_yaws[canvas_->start.first] = o1;
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

bool Tree::check_threshold(Node node, Node parent_, float yaw, float axis){
    /*
    float temp = INFINITY;
//    if(parents.find(std::pair(parent_, yaw)) == parents.end()){
////        std::cout << "BA";
//    }
    for(auto parent__: parents[std::pair(parent_, yaw)]){
        if(temp>std::min(Utils::get_angle(node, parent_, std::get<0>(parent__)), std::abs(360 - Utils::get_angle(node, parent_, std::get<0>(parent__))))){
            temp = std::min(Utils::get_angle(node, parent_, std::get<0>(parent__)), std::abs(360 - Utils::get_angle(node, parent_, std::get<0>(parent__))));
        }
    }
    return temp > 180 - threshold_theta;*/

    //std::cout<<"Got yaw "<<yaw<<" axis "<<axis<<std::endl;

    //AG: Implementation for 3D angle calcultation
    float temp = INFINITY;
    
    if(parents.find(std::tuple(parent_, yaw, axis)) == parents.end()){
          std::cout << "BA";
    }
    
    float a1 =  (std::get<0>(node) - std::get<0>(parent_));
    float a2 =  (std::get<1>(node) - std::get<1>(parent_));
    float a3 =  (std::get<2>(node) - std::get<2>(parent_));
    
    for(auto parent__: parents[std::tuple(parent_, yaw, axis)]){

        float b1 = (std::get<0>(parent_) - std::get<0>(std::get<0>(parent__)));
        float b2 = (std::get<1>(parent_) - std::get<1>(std::get<0>(parent__)));
        float b3 = (std::get<2>(parent_) - std::get<2>(std::get<0>(parent__)));
        //Calculate the angle between the 3D lines created by the nodes
        //Length of Parent_Current_Node vector = step_size
        float a1b1 =  a1*b1;
        float a2b2 =  a2*b2;
        float a3b3 =  a3*b3;

        //Calculate the length of two vectors
        float a_len =  std::sqrt(std::pow(a1,2) + std::pow(a2,2) + std::pow(a3,2));
        float b_len =  std::sqrt(std::pow(b1,2) + std::pow(b2,2) + std::pow(b3,2));
        
        float cos_angle_between_vectors =  (a1b1+a2b2+a3b3)/(a_len*b_len);
    
        if (cos_angle_between_vectors > 1)
           cos_angle_between_vectors = 1;
        else if(cos_angle_between_vectors < -1)
           cos_angle_between_vectors = -1;   
    
        float angle_between_vectors =  acos(cos_angle_between_vectors);
        
        if(temp > std::abs(angle_between_vectors))
           temp = std::abs(angle_between_vectors); 
    }

    bool feasibility = temp * 180/M_PI < threshold_theta; 
    
    //if(!feasibility)
    //   std::cout<<"check threshold "<<feasibility<<" Angle between vectors "<<temp*180/M_PI<<std::endl; 
    
    return feasibility;
}


bool Tree::add_node(Node parent_, Node node, float yaw, Gaussian *gauss){
    bool collision_free = true; //AG: This is to indicate if node addition is successful
    if(!canvas->check_collision(node, parent_, step_size)){
        bool flag = true;
        for (auto node_: nodes){
            bool plot_flag = true;
            //AG:Added to this code to avoid checking the condition on the nodes generated from same parent
            if(parent[node_] == parent_)
               continue;
            //AG: This is to reduce the node clutter & finiding if there exist another node in the vicinity
            if(Utils::eul_dist(node_, node) < step_size/pow(2,.5)){
                //AG: Adding extra loop for Axis search
                for(int axis=0; axis < TOTAL_AXIS; axis++){
                    for(int angle=0; angle<ceil(360/resolution_angle); angle++){
                        //AG: Checking kinematic constraint on the selected node
                        //if (Utils::feasible(parent_, yaw, node_, angle*resolution_angle, MAX_STEER_ANGLE)){
                        if (Utils::feasible_3D(parent_, canvas->end.first, node_, axis, angle*resolution_angle, MAX_STEER_ANGLE, step_size)){
                            //AG: Move to next iteration as this angle is already rejected
                            //if(rejected_yaws[node_][axis].find(angle*resolution_angle)==rejected_yaws[node_][axis].end()) {
                            if(std::find(rejected_yaws[node_][axis].begin(), rejected_yaws[node_][axis].end(), angle*resolution_angle)==rejected_yaws[node_][axis].end()) {
                                //if(available_yaws[node_][axis].find(angle*resolution_angle)==available_yaws[node_][axis].end()) {
                                if(std::find(available_yaws[node_][axis].begin(), available_yaws[node_][axis].end(), angle*resolution_angle)==available_yaws[node_][axis].end()) {
                                    //available_yaws[node_][axis].insert(angle * resolution_angle);
                                    available_yaws[node_][axis].push_back(angle * resolution_angle);
                                    //AG: Technically this will not happen
                                    if (actions.find(node_) == actions.end()) {
                                        //std::vector<float> v;
                                        Orientation n;
                                        actions[node_] = n;
                                    }
                                    if (std::find(actions[node_][axis].begin(), actions[node_][axis].end(), angle * resolution_angle) ==
                                        actions[node_][axis].end()) {
                                        actions[node_][axis].emplace_back(angle * resolution_angle);
                                        //AG: Adding this node_ to special_node list as this is leaf now a leaf node
                                        if (std::find(special_nodes.begin(), special_nodes.end(), node_) ==
                                            special_nodes.end()) {
                                            special_nodes.emplace_back(node_);

                                        }
                                    }
                                }
                            }
                            if (parents.find(std::tuple(node_, angle*resolution_angle, axis)) == parents.end()) {
                                std::set<std::tuple<Node, float, float>> s;
                                parents[std::tuple(node_, angle*resolution_angle, axis)] = s;
                            }
                            //AG: TODO Why this is updated even for the node which is in rejected yaw list
                            parents[std::tuple(node_, angle*resolution_angle, axis)].insert(std::tuple(parent_, yaw, gauss->axis));
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
                }
                flag = false;
                collision_free = false;
            }
        }
        if(flag){ //AG: Creating a new Node
            nodes.emplace_back(node);
            parent[node] = parent_;
            //std::vector<float> v;
            Orientation v;
            actions[node] = v;
            //std::set<float> s;
            Orientation s;
            available_yaws[node] = s;
            //std::set<float> s1;
            Orientation s1;
            rejected_yaws[node] = s1;
            for(int axis =0; axis < TOTAL_AXIS; axis++) {
                for(int angle=0; angle<ceil(360/resolution_angle); angle++){
                    //AG: Store all the possbile <node, action> pairs for the given <parent, yaw> combination
                    //AG: actions and available_yaw stores all the possible actions for the new node from <parent, yaw> pair
                    //if (Utils::feasible(parent_, yaw, node, angle*resolution_angle, MAX_STEER_ANGLE)){
                    if (Utils::feasible_3D(parent_, canvas->end.first, node, axis, angle*resolution_angle, MAX_STEER_ANGLE, step_size)){
                        //TODO: This if can be removed as the new node is just created
                        if(std::find(available_yaws[node][axis].begin(), available_yaws[node][axis].end(), angle*resolution_angle)==available_yaws[node][axis].end()){
                            //available_yaws[node][axis].insert(angle*resolution_angle);
                            available_yaws[node][axis].push_back(angle*resolution_angle);
                            if(actions.find(node)==actions.end()){
                                //std::vector<float> v;
                                Orientation v;
                                actions[node] = v;
                            }
                            if(parents.find(std::tuple(node, angle*resolution_angle, axis))==parents.end()){
                                std::set<std::tuple<Node, float, float>> s;
                                parents[std::tuple(node, angle*resolution_angle, axis)] = s;
                            }
                            parents[std::tuple(node, angle*resolution_angle, axis)].insert(std::tuple(parent_, yaw, gauss->axis));
                            if (std::find(actions[node][axis].begin(), actions[node][axis].end(),angle*resolution_angle)==actions[node][axis].end()){
                                actions[node][axis].emplace_back(angle*resolution_angle);
                            }
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
            if(parent[parent_]!=parent_ && check_threshold(node, parent_, yaw, gauss->axis)){
                fake = false;
                if (std::find(special_nodes.begin(), special_nodes.end(),parent_)!=special_nodes.end()){
                    special_nodes.erase(std::remove(special_nodes.begin(), special_nodes.end(), parent_), special_nodes.end());
                }
            }
            //if(fake){
            //    std::cout << "Parent Not Removed "<<std::get<0>(parent_)<<" "<<std::get<1>(parent_)<<std::endl;
            //}
        }
    } else{
        collision_free = false;
    }
    //TODO: Fix this implementation; check the functionality of the code
    //AG: Update the probabitlity of Parent node
    //change_proability(reinterpret_cast<Gaussian *>(&gauss));
    change_proability(gauss);

    return collision_free;
}

//AG: return value: is_sucessfull, node, yaw_direction
std::tuple<bool, Node, float> Tree::make_action(Node node, std::pair<float , Gaussian *> sampled_direction){
    if(actions.find(node) != actions.end()){
        //std::vector<float> actions_ = actions[node];
        Orientation actions_ = actions[node];
        if(actions_.empty()){
            actions.erase(node);
            // TODO:: change this
            return std::tuple(false, std::make_tuple(-1, -1, -1), -1);
        }
        //AG: Selecting the closest action on the selected Axis
        float closest = actions_[sampled_direction.second->axis][0];
        for(auto action: actions_[sampled_direction.second->axis]){
            if(Utils::dist_mean(action, sampled_direction.first) < Utils::dist_mean(closest, sampled_direction.first)){
                closest = action;
            }
        }
        Node sample = Utils::extend(node, canvas->end.first, step_size);
        sample = Utils::rotate(node, sample, closest, sampled_direction.second->axis, step_size);
        remove_action(node, closest, sampled_direction.second->axis);
        //rejected_yaws[node].insert(closest);
        rejected_yaws[node][sampled_direction.second->axis].push_back(closest);
        return std::make_tuple(true, sample, closest);
    }
    // TODO:: change this
    return std::make_tuple(false, std::make_tuple(-1, -1, -1), -1);
}

//AG: Remove the action from the current node which is used to generate a new sample
//Remove the node from special node list if all the actions are exhausted
void Tree::remove_action(Node node, float action, float axis) {
    std::vector<float> actions_ = actions[node][axis];
    // TODO: Remove nested loop
    if (std::find(actions_.begin(), actions_.end(),action)!=actions_.end()){
        actions[node][axis].erase(std::remove(actions[node][axis].begin(), actions[node][axis].end(), action), actions[node][axis].end());
    }
    
    //AG: Added new, this is to remove the axis if all the actions are exhausted
    if(actions[node][axis].empty()){
      actions[node].erase(axis); 
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

//AG: We are performing Breath first search. Starting from the end_node and parse all the possible configurations
//and save all the parent nodes and then expand these parent nodes furthur till we reach the start point and create 
//a child parent link in the reverse direction. Once start point is hit. Parse this parent-child link to get the path
void Tree::get_path(Node end_node) {
    struct Node_{
        std::tuple<Node, float, float> node_;
        std::tuple<Node, float, float> parent_;
        std::vector<std::tuple<Node, float, float>> childs;
    };
    std::vector<std::tuple<Node, float, float>> queue;
    std::map<std::tuple<Node, float, float>, Node_> nodes_;

    for(int axis =0; axis < TOTAL_AXIS; axis++) {
        for(int angle=0; angle<ceil(360/resolution_angle); angle++) {
            if(parents.find(std::tuple(end_node, angle*resolution_angle, axis))!=parents.end()){
                queue.emplace_back(std::tuple(end_node, angle*resolution_angle, axis));
                Node_ n;
                n.node_ = std::tuple(end_node, angle*resolution_angle, axis);
                n.parent_ = std::tuple(end_node, angle*resolution_angle, axis);
                nodes_[std::tuple(end_node, angle*resolution_angle, axis)] = n;
            }
        }
    }
    //AG: Breadth first search
    std::tuple<Node, float, float> current;
    std::map<std::tuple<Node, float, float>, bool> visited;
    while(true){
        current = queue.front();
        queue.erase(queue.begin());
        //TODO: Check for the Axis as well
        if(std::get<0>(current)==canvas->start.first && std::get<1>(current)==canvas->start.second && std::get<2>(current)== 0.){
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
                //std::ofstream myfile;
                //myfile.open ("removed.txt", std::ios_base::app);
                //myfile << std::get<0>(std::get<0>(parent__)) << " " << std::get<1>(std::get<0>(parent__)) <<"\n";
                //myfile.close();
            }
        }
    }
    //AG: Path is collection of pose, node position and axis, angle
    std::vector<std::tuple<Node, float, float>> path;
    while (std::get<0>(current)!=end_node){
        path.emplace_back(current);
        if(print_file){
            std::ofstream myfile;
            myfile.open ("path.txt", std::ios_base::app);
            myfile << std::get<0>(std::get<0>(current)) << " " << std::get<1>(std::get<0>(current)) <<"\n";
            myfile.close();
        }
        current = nodes_[current].parent_;
    }
    std::cout<<path.size()<<std::endl;
    std::cout<<"Path Search Ended"<<std::endl;
}

//AG: return: parent_node_, new_node_, direction_, parent_gaussian_  
std::tuple<Node, Node, float, Gaussian *> Tree::pick_random(int &iterations) {
    std::default_random_engine generator;
    generator.seed(time(0));
    //generator.seed();
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
        std::pair<float , Gaussian *> sample_direction = prob_dist[parent_].sample();
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
    float mean_shift = resolution_angle*.5f;
    gaussian->mean = Utils::shift_away(gaussian->mean,  0, mean_shift);
    float variance_shift = 2.f;
    gaussian->variance += variance_shift;
    gaussian->variance = fmax(20, gaussian->variance);
}
