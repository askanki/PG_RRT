//
// Created by Paras Sharma on 6/7/2020.
//

#ifndef UNTITLED2_UTILS_H
#define UNTITLED2_UTILS_H

#include <tuple>
#include "GMM.h"
#include <Eigen/Dense>
#include <Eigen/Geometry>
#include "config.h"

#define Node std::tuple<float, float, float>
#define Orientation std::map<float, std::vector<float>>  //Axis, yaw

class Utils {
public:
    static Node extend(Node start, Node end, float step_size);

    static Node rotate(Node root, Node node, float angle, float axis, float step_size);

    static float eul_dist(Node node1, Node node2);

    static void change_proability(Gaussian gauss, bool collision_free);

    static float shift_toward(float mean, float mean_, float shift);

    static float dist_mean(float node1_mean, float node2_mean);

    static float shift_away(float mean, float centre, float shift);

    static float get_angle(Node node, Node parent, Node parent_parent);

    static bool feasible(Node parent, float yaw, Node node, float angle, float max_turn);
    
    static bool feasible_3D(Node parent, Node end, Node node, float axis, float angle, float max_turn, float step_size);
};


#endif //UNTITLED2_UTILS_H
