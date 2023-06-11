#include <iostream>
#include <fstream>
#include <cmath>
#include <chrono>
#include "Canvas.h"
#include "Tree.h"
#include "Utils.h"

std::tuple<Tree*, Tree*, int> build_rrt(Tree *tree, Tree *tree1){
    int iterations = 0;
    auto timenow = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
    std::cout << "Start time: " << ctime(&timenow) << std::endl;
    std::chrono::high_resolution_clock::time_point t1 = std::chrono::high_resolution_clock::now();
    if(print_file) {
        std::ofstream myfile;
        myfile.open ("path_raw.txt");
        myfile << std::get<0>(tree->canvas->start.first) << " " << std::get<1>(tree->canvas->start.first) <<" "<< std::get<2>(tree->canvas->start.first)<< std::endl;
        myfile << std::get<0>(tree1->canvas->start.first) << " " << std::get<1>(tree1->canvas->start.first) <<" "<<std::get<2>(tree1->canvas->start.first)<< std::endl;
        myfile.close();
        std::ofstream myfile1;
        myfile1.open ("removed.txt");
        myfile1.close();
        std::ofstream myfile2;
        myfile2.open ("kino.txt");
        myfile2.close();
        std::ofstream myfile3;
        myfile3.open ("path.txt");
        myfile3.close();
    }
    while(iterations < MAX_ITERATION){
        //AG: return: parent_node_, new_node_, direction_, parent_gaussian_
        std::tuple<Node, Node, float, Gaussian *> par_node_yaw_gauss = tree->pick_random(iterations);
        bool change = tree->add_node(std::get<0>(par_node_yaw_gauss), std::get<1>(par_node_yaw_gauss), std::get<2>(par_node_yaw_gauss), std::get<3>(par_node_yaw_gauss));
        //TODO: Code only works when both the trees expand
        //std::tuple<Node, Node, float,  Gaussian *> par_node_yaw_gauss1 = tree1->pick_random(iterations);
        //bool change1 = tree1->add_node(std::get<0>(par_node_yaw_gauss1), std::get<1>(par_node_yaw_gauss1), std::get<2>(par_node_yaw_gauss1), std::get<3>(par_node_yaw_gauss1));
        std::tuple<Node, Node, float,  Gaussian *> par_node_yaw_gauss1; 
        bool change1 = false;

        if(change){
            if(print_file) {
                std::ofstream myfile;
                myfile.open ("path_raw.txt", std::ios_base::app);
                myfile << std::get<0>(std::get<1>(par_node_yaw_gauss)) << " " << std::get<1>(std::get<1>(par_node_yaw_gauss)) << " " << std::get<2>(std::get<1>(par_node_yaw_gauss)) <<" "
                       << std::get<0>(std::get<0>(par_node_yaw_gauss)) << " " << std::get<1>(std::get<0>(par_node_yaw_gauss)) << " " << std::get<2>(std::get<0>(par_node_yaw_gauss)) << "\n";
                myfile.close();
            }
            //AG: Check for convergence; if the new node is close to the End node of Tree
            if(Utils::eul_dist(std::get<1>(par_node_yaw_gauss), tree->canvas->end.first) <= tree->step_size){
                std::chrono::high_resolution_clock::time_point t2 = std::chrono::high_resolution_clock::now();
                std::chrono::duration<double, std::milli> time_span = t2 - t1;
                std::cout << "Search time: " << time_span.count() << std::endl;
                auto timenow = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
                std::cout << "End time search: " << ctime(&timenow) << std::endl;
                tree->get_path(std::get<1>(par_node_yaw_gauss));
                break;
            }
            //AG: Check for convergence; if the two tree nodes are close 
            bool flag = false;
            for(auto node: tree1->nodes){
                if (Utils::eul_dist(std::get<1>(par_node_yaw_gauss), node) < tree->step_size/(pow(2, 0.5))){
                    flag = true;
                    std::chrono::high_resolution_clock::time_point t2 = std::chrono::high_resolution_clock::now();
                    std::chrono::duration<double, std::milli> time_span = t2 - t1;
                    std::cout << "Search time: " << time_span.count() << std::endl;
                    auto timenow = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
                    std::cout << "End time search: " << ctime(&timenow) << std::endl;
                    tree->get_path(std::get<1>(par_node_yaw_gauss));
                    tree1->get_path(node);
                }
            }
            if (flag){break;}
        }
        if(change1){
            if(print_file) {
                std::ofstream myfile;
                myfile.open ("path_raw.txt", std::ios_base::app);
                myfile << std::get<0>(std::get<1>(par_node_yaw_gauss1)) << " " << std::get<1>(std::get<1>(par_node_yaw_gauss1)) << " " << std::get<2>(std::get<1>(par_node_yaw_gauss1)) << " "
                       << std::get<0>(std::get<0>(par_node_yaw_gauss1)) << " " << std::get<1>(std::get<0>(par_node_yaw_gauss1)) << " " << std::get<2>(std::get<0>(par_node_yaw_gauss1)) << "\n";
                myfile.close();
            }
            //AG: Check for convergence; if the new node is close to the End node of Tree-1
            if(Utils::eul_dist(std::get<1>(par_node_yaw_gauss1), tree1->canvas->end.first) < tree1->step_size){
                std::chrono::high_resolution_clock::time_point t2 = std::chrono::high_resolution_clock::now();
                std::chrono::duration<double, std::milli> time_span = t2 - t1;
                std::cout << "Search time: " << time_span.count() << std::endl;
                auto timenow = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
                std::cout << "End time search: " << ctime(&timenow) << std::endl;
                tree1->get_path(std::get<1>(par_node_yaw_gauss1));
                break;
            }
            //AG: Check for convergence; if the two tree nodes are close 
            bool flag = false;
            for(auto node: tree->nodes){
                if (Utils::eul_dist(std::get<1>(par_node_yaw_gauss1), node) < tree1->step_size/(pow(2, 0.5))){
                    flag = true;
                    std::chrono::high_resolution_clock::time_point t2 = std::chrono::high_resolution_clock::now();
                    std::chrono::duration<double, std::milli> time_span = t2 - t1;
                    std::cout << "Search time: " << time_span.count() << std::endl;
                    auto timenow = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
                    std::cout << "End time search: " << ctime(&timenow) << std::endl;
                    tree1->get_path(std::get<1>(par_node_yaw_gauss1));
                    tree->get_path(node);
                }
            }
            if (flag){break;}
        }
//        if (iterations%100==0){std::cout<<iterations<<std::endl;}
    }
    return std::make_tuple(tree, tree1, iterations);
}

int main() {
    float iter_ts_pcost[4] = {0., 0., 0., 0.};
    for(int count=1; count<=1; count++) {
        //Scenario - 1
        // Canvas canvas;
        // canvas.start = Node(5.f, 5.f);
        // canvas.end = Node(15.f, 15.f);
        // canvas.add_obs_from_file("../Scenario_1.txt");
        // Tree tree(&canvas, SP_THRESHOLD, RESOLUTION, STEP_SIZE);

        // Canvas canvas1;
        // canvas1.end = Node(5.f, 5.f);
        // canvas1.start = Node(15.f, 15.f);
        // canvas1.add_obs_from_file("../Scenario_1.txt");
        // Tree tree1(&canvas1, SP_THRESHOLD, RESOLUTION, STEP_SIZE);

        //Scenario - 3
        Canvas canvas;
        //std::pair<Node, float> start = std::pair(Node(2.0f, 15.f, 0.), 0.f); //start/end format - coordinate, yaw
        //std::pair<Node, float> end = std::pair(Node(35.f, 17.f, 0.), 0.f);   //start/end format - coordinate, yaw
        std::pair<Node, float> start = std::pair(Node(10.f, 15.f, 0.), 30.f);   //start/end format - coordinate, yaw
        std::pair<Node, float> end = std::pair(Node(35.f, 17.f, 0.), -30.f);    //start/end format - coordinate, yaw
        canvas.start = start;
        canvas.end = end;
        canvas.add_obs_from_file("../map");
        Tree tree(&canvas, SP_THRESHOLD, RESOLUTION, STEP_SIZE);

        Canvas canvas1;
        canvas1.end = start;;
        canvas1.start = end;
        canvas1.add_obs_from_file("../map");
        Tree tree1(&canvas1, SP_THRESHOLD, RESOLUTION, STEP_SIZE);


        //Scenario - 2
        // Canvas canvas;
        // canvas.start = Node(1.f, 0.f);
        // canvas.end = Node(13.f, -5.f);
        // canvas.add_obs_from_file("../H.txt");
        // Tree tree(&canvas, SP_THRESHOLD, RESOLUTION, STEP_SIZE);

        // Canvas canvas1;
        // canvas1.end = Node(1.f, 0.f);
        // canvas1.start = Node(13.f, -5.f);
        // canvas1.add_obs_from_file("../H.txt");
        // Tree tree1(&canvas1, SP_THRESHOLD, RESOLUTION, STEP_SIZE);
       
        //Scenario - 4
        // Canvas canvas;
        // canvas.start = Node(2.f, 0.f);
        // canvas.end = Node(27.f, 13.f);
        // canvas.add_obs_from_file("../Scenario_4.txt");
        // Tree tree(&canvas, SP_THRESHOLD, RESOLUTION, STEP_SIZE);

        // Canvas canvas1;
        // canvas1.end = Node(2.f, 0.f);
        // canvas1.start = Node(27.f, 13.f);
        // canvas1.add_obs_from_file("../Scenario_4.txt");
        // Tree tree1(&canvas1, SP_THRESHOLD, RESOLUTION, STEP_SIZE);

        std::chrono::high_resolution_clock::time_point t1 = std::chrono::high_resolution_clock::now();
        std::tuple<Tree *, Tree *, int> tree_iter = build_rrt(&tree, &tree1);
        auto timenow = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
        std::chrono::high_resolution_clock::time_point t2 = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double, std::milli> time_span = t2 - t1;
        iter_ts_pcost[1] += (time_span.count() - iter_ts_pcost[1])/count;
        iter_ts_pcost[0] += (std::get<2>(tree_iter) - iter_ts_pcost[0])/count;
        iter_ts_pcost[2] += iter_ts_pcost[2]/count;
        iter_ts_pcost[3] += (std::get<0>(tree_iter)->nodes.size()+std::get<1>(tree_iter)->nodes.size() - iter_ts_pcost[3])/count;
        std::cout << "End time: " << ctime(&timenow) << std::endl;
        std::cout << "Time spent: " << time_span.count() << " ms" << std::endl;
        std::cout << "Iterations: " << std::get<2>(tree_iter) << std::endl << std::flush;
    }
    std::cout << "Average time: " << iter_ts_pcost[1] << std::endl;
    std::cout << "Average iterations: " << iter_ts_pcost[0] << std::endl;
    std::cout << "Average nodes: " << iter_ts_pcost[3] << std::endl;
    return 0;
}