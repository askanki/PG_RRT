//
// Created by Paras Sharma on 6/7/2020.
//
#include <math.h>
#include <iostream>
#include "Utils.h"

Node Utils::extend(Node start, Node end, float step_size) {
    float distance = eul_dist(start, end);
    float ratio = step_size/distance;
    return std::make_tuple((1 - ratio) * std::get<0>(start) + ratio * std::get<0>(end),
            ((1 - ratio) * std::get<1>(start) + ratio * std::get<1>(end)),
            ((1 - ratio) * std::get<2>(start) + ratio * std::get<2>(end)));
}

Node Utils::rotate(Node root, Node node, float angle, float axis){
    // roll, yaw, pitch
    angle *= M_PI / 180;
    float ox = std::get<0>(root);
    float oy = std::get<1>(root);
    float px = std::get<0>(node);
    float py = std::get<1>(node);
    float qx = ox + cos(angle) * (px - ox) - sin(angle) * (py - oy);
    float qy = oy + sin(angle) * (px - ox) + cos(angle) * (py - oy);
    return std::make_tuple(qx, qy, 0);
}

float Utils::eul_dist(Node node1, Node node2) {
    return sqrt(pow(std::get<0>(node1) - std::get<0>(node2), 2) +  pow(std::get<1>(node1) - std::get<1>(node2), 2));
}

float Utils::shift_toward(float mean, float centre, float shift) {
    if(abs(dist_mean(mean-shift, centre)) <= abs(dist_mean(mean+shift, centre))){
        mean-=shift;
    } else{
        mean+=shift;
    }
    return remainder(mean, 360);
}

float Utils::shift_away(float mean, float centre, float shift) {
    if(abs(dist_mean(mean-shift, centre)) <= abs(dist_mean(mean+shift, centre))){
        mean+=shift;
    } else{
        mean-=shift;
    }
    return remainder(mean, 360);
}

float Utils::dist_mean(float node1_mean, float node2_mean) {
//    std::cout << fmin(fmod(fabs(node1_mean - node2_mean), 360), fmod(360 - fabs(node1_mean - node2_mean), 360)) << "Node mean " << node1_mean<< std::endl;
    return fmin(fmod(fabs(node1_mean - node2_mean), 360), fmod(360 - fabs(node1_mean - node2_mean), 360));
}

float Utils::get_angle(Node a, Node b, Node c) {
    float ang = (180 / M_PI) * (atan2(std::get<1>(c) - std::get<1>(b), std::get<0>(c) - std::get<0>(b)) -
                                atan2(std::get<1>(a) - std::get<1>(b), std::get<0>(a) - std::get<0>(b)));
    if (ang < 0){
        return ang + 360;
    }
    else {
        return ang;
    }
}

bool Utils::feasible(Node parent, float yaw, Node node, float angle, float max_turn) {
    return dist_mean(yaw, angle) <= max_turn;
//    return true;
}



