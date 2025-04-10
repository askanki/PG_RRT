//
// Created by Paras Sharma on 6/7/2020.
//

#ifndef PGRRT_CANVAS_H
#define PGRRT_CANVAS_H

#include <tuple>
#include <vector>
#define Node std::tuple<float, float>

class Canvas {

public:
    //start/end format - coordinate, yaw
    std::pair<Node, float> start;
    std::pair<Node, float> end;
    std::vector <Node> obs_points;
    void add_obstacles(std::vector <Node> obs);
    void add_obs_from_file(std::string path_to_file);
    bool check_collision(std::tuple<float, float> node1, std::tuple<float, float> node2, float step_size);
};


#endif //PGRRT_CANVAS_H
