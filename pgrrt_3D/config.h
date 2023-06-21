//
// Created by Paras Sharma on 10/26/2020.
//

#ifndef UNTITLED2_CONFIG_H
#define UNTITLED2_CONFIG_H

#define RESOLUTION 45.        //AG: This parameter is to disretize the action space
#define SP_THRESHOLD 180.     //AG: This parameter is to identify the Special node
#define MAX_STEER_ANGLE 60.  //AG: Kino constraint of the vehicle
#define STEP_SIZE 3.f         //AG: Step size is 0.5 in 2D case 
#define MAP_RESOLUTION 1.f
#define TOTAL_AXIS 2
#define print_file true
#define MAX_ITERATION 100000
#define USE_OCOTMAP 1
#define WRITE_OCTOMAP_FROM_FILE 0
#define NUMBER_OF_GAUSSIAN_PER_AXIS 2 //Not completely implemented
#define INITIAL_GAUSSIAN_VARIANCE 20. 
#define INITIAL_GAUSSIAN_MEAN 15. 
#define MAX_GAUSSIAN_VARIANCE 60. 

#if (TOTAL_AXIS == 1)
//Algo performance important Parameter
#define CHILD_MEAN_SHIFT_PERCENTAGE  0.2
#define CHILD_VAR_SHIFT_PERCENTAGE   0.075
#define PARENT_MEAN_SHIFT_PERCENTAGE 0.2
#define PARENT_VAR_SHIFT_PERCENTAGE  0.1
#else
//Algo performance important Parameter
#define CHILD_MEAN_SHIFT_PERCENTAGE  0.1
#define CHILD_VAR_SHIFT_PERCENTAGE   0.1
#define PARENT_MEAN_SHIFT_PERCENTAGE 0.1
#define PARENT_VAR_SHIFT_PERCENTAGE  0.1
#endif



#endif //UNTITLED2_CONFIG_H

