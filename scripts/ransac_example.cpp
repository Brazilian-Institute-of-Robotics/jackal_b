int main()
{
    //cv::Mat color = cv::imread("../inputData/semi_circle_contrast.png");
    cv::Mat color = cv::imread("../inputData/semi_circle_median.png");
    cv::Mat gray;

    // convert to grayscale
    cv::cvtColor(color, gray, CV_BGR2GRAY);

    // now map brightest pixel to 255 and smalles pixel val to 0. this is for easier finding of threshold
    double min, max;
    cv::minMaxLoc(gray,&min,&max);
    float sub = min;
    float mult = 255.0f/(float)(max-sub);
    cv::Mat normalized = gray - sub;
    normalized = mult * normalized;
    cv::imshow("normalized" , normalized);
    //--------------------------------


    // now compute threshold
    // TODO: this might ne a tricky task if noise differs...
    cv::Mat mask;
    //cv::threshold(input, mask, 0, 255, CV_THRESH_BINARY | CV_THRESH_OTSU);
    cv::threshold(normalized, mask, 100, 255, CV_THRESH_BINARY);



    std::vector<cv::Point2f> edgePositions;
    edgePositions = getPointPositions(mask);

    // create distance transform to efficiently evaluate distance to nearest edge
    cv::Mat dt;
    cv::distanceTransform(255-mask, dt,CV_DIST_L1, 3);

    //TODO: maybe seed random variable for real random numbers.

    unsigned int nIterations = 0;

    cv::Point2f bestCircleCenter;
    float bestCircleRadius;
    float bestCirclePercentage = 0;
    float minRadius = 50;   // TODO: ADJUST THIS PARAMETER TO YOUR NEEDS, otherwise smaller circles wont be detected or "small noise circles" will have a high percentage of completion

    //float minCirclePercentage = 0.2f;
    float minCirclePercentage = 0.05f;  // at least 5% of a circle must be present? maybe more...

    int maxNrOfIterations = edgePositions.size();   // TODO: adjust this parameter or include some real ransac criteria with inlier/outlier percentages to decide when to stop

    for(unsigned int its=0; its< maxNrOfIterations; ++its)
    {
        //RANSAC: randomly choose 3 point and create a circle:
        //TODO: choose randomly but more intelligent, 
        //so that it is more likely to choose three points of a circle. 
        //For example if there are many small circles, it is unlikely to randomly choose 3 points of the same circle.
        unsigned int idx1 = rand()%edgePositions.size();
        unsigned int idx2 = rand()%edgePositions.size();
        unsigned int idx3 = rand()%edgePositions.size();

        // we need 3 different samples:
        if(idx1 == idx2) continue;
        if(idx1 == idx3) continue;
        if(idx3 == idx2) continue;

        // create circle from 3 points:
        cv::Point2f center; float radius;
        getCircle(edgePositions[idx1],edgePositions[idx2],edgePositions[idx3],center,radius);

        // inlier set unused at the moment but could be used to approximate a (more robust) circle from alle inlier
        std::vector<cv::Point2f> inlierSet;

        //verify or falsify the circle by inlier counting:
        float cPerc = verifyCircle(dt,center,radius, inlierSet);

        // update best circle information if necessary
        if(cPerc >= bestCirclePercentage)
            if(radius >= minRadius)
        {
            bestCirclePercentage = cPerc;
            bestCircleRadius = radius;
            bestCircleCenter = center;
        }

    }

    // draw if good circle was found
    if(bestCirclePercentage >= minCirclePercentage)
        if(bestCircleRadius >= minRadius);
        cv::circle(color, bestCircleCenter,bestCircleRadius, cv::Scalar(255,255,0),1);


        cv::imshow("output",color);
        cv::imshow("mask",mask);
        cv::waitKey(0);

        return 0;
    }