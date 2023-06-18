//
// Created by Paras Sharma on 6/7/2020.
//

#include <fstream>
#include <iostream>
#include <sstream>
#include <iterator>
#include <cmath>
#include "Canvas.h"
#include "Utils.h"

bool Canvas::check_collision(Node node1, Node node2, float step_size) {
    if (USE_OCOTMAP) {
        point3d pt3D_node(std::get<0>(node1), std::get<1>(node1), std::get<2>(node1)); 
        point3d pt3D_parent(std::get<0>(node2), std::get<1>(node2), std::get<2>(node2)); 

        /*
        //AG: This is a Ray casting code to find the intersection point. But this doesn't work well
        //RG_RRT is passing throught the obstacles
        point3d pt3D_direction = pt3D_node - pt3D_parent;
        point3d ray_end;

        bool collision_status = obsmap->castRay(pt3D_node, pt3D_direction, ray_end, false, step_size*1.2);
       
        if(collision_status){
          std::cout<<"Collison Detected :"<< std::get<0>(node1) <<" "<< std::get<1>(node1)<<" "<<std::get<2>(node1)<<std::endl;
          std::cout << "ray hit cell with center " << ray_end << std::endl;      
        }*/

        //AG: OcotoMap Eucladian Distance Transform to find the nearest neighbour
        //This is how you can query the map
        octomap::point3d closestObst;
        float distance;
        bool collision_status = false; 

        //AG: Check if the generate point is out of map
        if((pt3D_node.x() > max_x) || (pt3D_node.x() < min_x) || (pt3D_node.y() > max_y) || (pt3D_node.y() < min_y) || (pt3D_node.z() > max_z) || (pt3D_node.z() < min_z)) 
        {
            collision_status = true;
            //std::cout<<"Crossed Boundary"<<std::endl;
            return(collision_status);
        }

        obsdistmap->getDistanceAndClosestObstacle(pt3D_node, distance, closestObst);
   
        //std::cout<<"\n\ndistance at point "<<pt3D_node.x()<<","<<pt3D_node.y()<<","<<pt3D_node.z()<<" is "<<distance<<std::endl;
        
        if(distance < step_size/pow(2, .5))  {
              // std::cout<<"Closest obstacle to "<<pt3D_node.x()<<","<<pt3D_node.y()<<","<<pt3D_node.z()<<" is at "<<closestObst.x()<<","<<closestObst.y()<<","<<closestObst.z()<<std::endl;
              //std::cout<<"\nObstacle distance at point is :"<<distance<<std::endl;
              collision_status = true;
        }
        
         
        return(collision_status);
    }
    else {
        for(auto obs: obs_points){
            if(Utils::eul_dist(node1, obs) < step_size/pow(2, .5)){
                return true;
            }
        }
        return Utils::eul_dist(node1, node2) < step_size/pow(2, .5);
    }
}

void Canvas::add_obstacles(std::vector<Node> obs) {
    obs_points = obs;
}

void Canvas::add_obs_from_file(std::string path_to_file) {
    std::string line;
    std::string word;
    std::ifstream obs_file (path_to_file);
    
    if(WRITE_OCTOMAP_FROM_FILE) {
        OcTree ObsTree(.1);
        obsmap = new OcTree(ObsTree);
    }

    if (obs_file.is_open())
    {
        while (getline (obs_file,line))
        {
            std::vector<float> v;
            std::istringstream line_(line);
            std::copy(std::istream_iterator<float>(line_),
                      std::istream_iterator<float>(),
                      std::back_inserter(v));
            //obs_points.emplace_back(v[0], v[1], v[2]);
            obs_points.emplace_back(v[0], v[1], 0.);
            
            if(WRITE_OCTOMAP_FROM_FILE)
            {
                point3d pt3D(v[0], v[1], 0.);
                obsmap->updateNode(pt3D, true); 
            }
        }
        obs_file.close();
        
        if(WRITE_OCTOMAP_FROM_FILE)
           obsmap->write("octomap_from_file.ot");
    }

    else std::cout << "Unable to open file";
}

void Canvas::add_obs_from_octomap(std::string path_to_file) {
    
    //Read the Octree file in the AbstractOcTree class and perfrom dynamic cast
    AbstractOcTree* readTreeAbstract = AbstractOcTree::read(path_to_file);
    obsmap = dynamic_cast<OcTree*>(readTreeAbstract);
    //std::cout<<"Octree File read :"<<path_to_file<<std::endl;
    //std::cout<<"Octree Resolution :"<<obsmap->getResolution()<<std::endl;
    
    //Update Tree Resolution
    //obsmap->setResolution(MAP_RESOLUTION);    
    //std::cout<<"Updated Octree Resolution :"<<obsmap->getResolution()<<std::endl;
    
    obsmap->getMetricMin(min_x,min_y,min_z);
    octomap::point3d min(min_x,min_y,min_z);
    std::cout<<"Metric min: "<<min_x<<","<<min_y<<","<<min_z<<std::endl;
    obsmap->getMetricMax(max_x,max_y,max_z);
    octomap::point3d max(max_x,max_y,max_z);
    std::cout<<"Metric max: "<<max_x<<","<<max_y<<","<<max_z<<std::endl;

    bool unknownAsOccupied = true;
    unknownAsOccupied = false;
    float maxDist = STEP_SIZE;
    //- the first argument ist the max distance at which distance computations are clamped
    //- the second argument is the octomap
    //- arguments 3 and 4 can be used to restrict the distance map to a subarea
    //- argument 5 defines whether unknown space is treated as occupied or free
    //The constructor copies data but does not yet compute the distance map
    obsdistmap = new DynamicEDTOctomap(maxDist, obsmap, min, max, unknownAsOccupied);
    //Generate the distance map
    obsdistmap->update();

    std::cout<<"Max distance in dist map :"<<obsdistmap->getMaxDist()<<std::endl;
    std::cout<<"\n\n";
    //exit(0);
}
