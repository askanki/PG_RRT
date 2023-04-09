//
// Created by Paras Sharma on 6/7/2020.
//

#ifndef UNTITLED2_UTILS_H
#define UNTITLED2_UTILS_H

#include <tuple>
#include "GMM.h"
#include "eigen/Eigen/Dense"
#include "eigen/Eigen/Geometry"

#define Node std::tuple<float, float, float>

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
};


#endif //UNTITLED2_UTILS_H
