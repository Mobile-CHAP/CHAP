#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <string>
#include <ctime>

using namespace cv;
using namespace std;

string imgDir = "./public/stream/";
char buffer [L_tmpnam];

int main (int argc, char** argv)
{	
	if(argc < 2)
		return - 1;
	
	VideoCapture cap(0); // open the default camera
	if (!cap.isOpened())  // check if we succeeded
		return -1;
	
	Mat frame;
	cap >> frame; // get a new frame from camera
	cap >> frame; // Next frame to allow for auto camera adjustment

	string imageName = "newImage" + string(argv[1]); //need random name
	imwrite(imgDir+imageName+".jpg",frame);
	
	cout << imageName;
	return 0;
}