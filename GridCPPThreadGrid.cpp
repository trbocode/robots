#include <cmath>
#include <iomanip>
#include <iostream>
#include <map>
#include <random>
#include <string>
#include <thread>
#include <vector>
#include <fstream>


void rem(double* curr, double mod) {
    if (*curr < 0) {
        *curr+=mod;
    }
}
int wrap_slope(double curr[]) {
    return (curr[0] > curr[1]+0.5 || (curr[0]< curr[1] && curr[0]>curr[1]-0.5));
}
int wrap2_slope(double curr[]){
	double x=curr[0];
	double y=curr[1];
	return ((4*x+0.75>y &&  4*x+0.25<y) || (4*(x-0.0625)>y && 4*(x-0.1875)<y) || (4*(x-0.3125)>y && 4*(x-0.4375)<y) || (4*(x-0.5625)>y && 4*(x-0.6875)<y) || (4*(x-0.8125)>y && 4*(x-0.9375)<y)); 
}
int slope(double curr[], double slope) {
    return curr[0] < (0.5+slope*curr[1]-0.5*slope);
}
int double_slope(double curr[]) {
    return (curr[0] < curr[1] == 1-curr[0] < curr[1]);
}
int reverse_slope(double curr[]) {
    return 1-curr[0] > curr[1];
}
int halfgrid(double curr[], double grid) {
    return (std::fmod(curr[0], grid)
     < grid/2 && std::fmod(curr[1], grid) < grid/2);
}
int agrid(double curr[], double grid) {
    return ((std::fmod(curr[0], grid) < grid/2)
     == (std::fmod(curr[1], grid) < grid/2));
}
int triangle(double curr[]) {
    return (curr[1] < 1/sqrt(2)-curr[0] || curr[1]>2-1/sqrt(2)-curr[0]);
}

void brownian(double *ran, double mean, int64_t len,
   double dt, double delta, double torus) {
    std::random_device rd{};
    std::mt19937 gen{rd()};
    std::normal_distribution<double> d{mean, delta*sqrt(dt)};
    for (int i=0; i < len; i++) {
        ran[i]=(std::fmod(d(gen), torus));
    }
}

void simulation(double grid, double speed) {
    double *x, *x1, *y, *y1;
    int64_t N = 100000000;
    int64_t maxN = 10000000;
    int64_t printN = 1000000000;
    int matsize=100;
    x = reinterpret_cast<double*>(malloc(maxN*sizeof(double)));
    x1 = reinterpret_cast<double*>(malloc(maxN*sizeof(double)));
    y = reinterpret_cast<double*>(malloc(maxN*sizeof(double)));
    y1 = reinterpret_cast<double*>(malloc(maxN*sizeof(double)));
    long *mat = (long *)malloc(matsize * matsize * sizeof(long));
    long *line = (long *)malloc(100 * sizeof(long));
    long **density=(long**)malloc(matsize * sizeof(long*));
    for (int i=0;i<matsize;i++){
        density[i]=mat+matsize*i;
    }
    double dt = 1/static_cast<double>(1000000);
    double torus = 1;
    double curr[2] = {(static_cast<double>(rand()) / (RAND_MAX)),
    (static_cast<double>(rand()) / (RAND_MAX))};
    int64_t xs = 0;
    int64_t ys = 0;
    int64_t xold = 0;
    int64_t yold = 0;
    std::ofstream out;
    out.open("Speed"+std::to_string(speed)+" Grid"+std::to_string(grid)+".txt");
    for (int64_t i=0; i < N; i++) {
        int64_t j = i%maxN;
        if (j == 0) {
            brownian(x, 0, maxN, dt, 1, torus);
            brownian(x1, 0, maxN, dt, 1, torus);
            brownian(y, 0, maxN, dt, 1, torus);
            brownian(y1, 0, maxN, dt, speed, torus);
            if ((i % printN) == 0) {
                if (ys != yold) {
                //    out << std::setprecision(15) <<
                //    (static_cast<double>(xs-xold)/(ys-yold)) << "\n";
                } else if (xs != xold) {
                //    out << (xs-xold) << "\n";
                }
                out.flush();
                xold = xs;
                yold = ys;
            }
        }
        density[int(curr[0]*matsize)][int(curr[1]*matsize)]++;
        if (agrid(curr,1)) {
            line[int(curr[0]/0.01)]++;
            curr[0]+=y[j];
            curr[1]+=y1[j];
            ys++;
        } else {
            curr[0]+=x[j];
            curr[1]+=x1[j];
            xs++;
        }
        curr[0] = std::fmod(curr[0], torus);
        curr[1] = std::fmod(curr[1], torus);
        rem(curr, torus);
        rem(curr+1, torus);
    }
    if ((ys-yold) != 0) {
        out << std::setprecision(15) <<
            (static_cast<double>(xs-xold)/(ys-yold)) <<"\n";
    }
    if (ys != 0) {
        out << std::setprecision(15) <<
            (static_cast<double>(xs)/ys) <<"\n";
    }
    //out << "{";
    for(int i=0;i<matsize;i++){
        //long sumx=0;
        //long sumy=0;
        //out << "{";
        for(int j=0;j<matsize;j++){
            /*double arr1[2]={i*0.1,j*0.1};
            double arr2[2]={i*0.1,0.1+j*0.1};
            if(slope(arr1,grid) && slope(arr2,grid)){
                out << "Fast "+std::to_string(i)+std::to_string(j)+" "<< std::setprecision(15) << (static_cast<double>(density[i][j])/N) <<"\n";
            }
            else if(slope(arr1,grid) || slope(arr2,grid)){
                out << "Mid "+std::to_string(i)+std::to_string(j)+" "<< std::setprecision(15) << (static_cast<double>(density[i][j])/N) <<"\n";
            }
            else{
                out << "Slow "+std::to_string(i)+std::to_string(j)+" "<< std::setprecision(15) << (static_cast<double>(density[i][j])/N) <<"\n";
            }
            sumx+=density[i][j];
            sumy+=density[j][i];*/
            out << std::setprecision(15) << (static_cast<double>(density[i][j])/N);
            if(j!=matsize-1){
                out << " ";
            }
            else{
                out << "\n";
            }
        }
        //out << "X "+std::to_string(i)+" "<< std::setprecision(15) << (static_cast<double>(sumx)/N) <<"\n";
        //out << "Y "+std::to_string(i)+" "<< std::setprecision(15) << (static_cast<double>(sumy)/N) <<"\n";
    }
    for(int i=0;i<100;i++){
        //out << "Line "+std::to_string(i)+" "<< std::setprecision(15) << (static_cast<double>(line[i])/N) <<"\n";
    }
    free(x);
    free(x1);
    free(y);
    free(y1);
    free(density);
    free(mat);
    free(line);
}


int main() {
    //double grids[] = {0.1, 0.2, 0.3, 0.5, 0.8, 1, 1.25, 2.0, 3.3333, 5.0, 10.0};
    double grids[] = {576};
    // double grids[] = {0.1, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0};
    double speeds[] = {0.125,0.25,0.5,2,4,8,16};
    std::vector<std::thread> threads;
    for (double speed : speeds) {
        for (double grid : grids)
            threads.emplace_back(std::thread(simulation, grid, speed));    
    }
    for (auto &t : threads)
        t.join();
    threads.clear();
    return 0;
}
