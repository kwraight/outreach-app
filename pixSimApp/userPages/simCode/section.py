### simple pixel charge sharing simulation
import numpy as np
import math
import random

class Point:
    def __init__(self, x, y, c):
        self.x=x
        self.y=y
        self.c=c
    def Set(self, x, y, c):
        self.x=x
        self.y=y
        self.c=c
    def SpitPoint(self):
        print("(",self.x,",",self.y,",",self.z,")")

#############
# circles
#############

def TranslatePoint(p, centX, centY): # area of circle section (chorded off bit)
    p.x = p.x - centX
    p.y = p.y - centY


def CalcSecArea(rad, ang): # area of circle section (chorded off bit) // assumes centre at 0,0
    return (rad*rad/2) * ( (ang*np.pi/180) - sin(ang*np.pi/180))


def CalcSegArea(rad, ang): # area of circle segment (cake slice) // assumes centre at 0,0
    return np.pi * rad*rad * (ang/360)


def CalcRecArea(x, y): # area of rectangle
    return x * y


def CalcChordLength(rad, ang):
    return rad * sqrt( 2 - 2*cos(ang*PI/180) )


def CalcChordLength(p1, p2):
    double dx = p1->x - p2->x
    double dy = p1->y - p2->y
    length = sqrt( (dx*dx) + ( dy*dy ) )
    # print("dx:",dx,"\tdy:",dy,"\tlength:",length)
    return length


def CalcSecAngle(rad, p1, p2):# assumes centre at 0,0
    angle = np.asin( CalcChordLength( p1, p2 ) / (2*rad) ) * 2; # in radians
    # print("ratio:",CalcChordLength( p1, p2 ) / (2*rad),"\tasin:",asin(2))
    # print("angle(rad):",angle)
    angle = angle * 180/np.pi
    # print("angle(deg):",angle)
    return angle


def CalcSecAngle(rad, length ): # assumes centre at 0,0
    angle = asin( length / (2*rad) ) * 2 # in radians
    # print("ratio:",CalcChordLength( p1, p2 ) / (2*rad),"\tasin:",asin( 2))
    # print("angle(rad):",angle)
    angle = angle * 180/np.pi
    # print("angle(deg):",angle)
    return angle


def CalcSecAngle(rad, centX, centY, p1, p2 ):
    tp1=Point(p1.x, p1.y) # adjust for non-zero - centre
    TranslatePoint( tp1.x, centX, centY )
    tp2=Point(p2.x, p2.y)
    TranslatePoint(p2.x, centX, centY )
    angle = asin( CalcChordLength( tp1, tp2 ) / (2*rad) ) * 2 # in radians
    # cout<<"ratio: "<<CalcChordLength( p1, p2 ) / (2*rad) <<"\tasin: "<<asin( 2) <<endl;
    //cout<<"angle(rad): "<<angle<<endl;
    angle = angle * 180/PI;
    //cout<<"angle(deg): "<<angle<<endl;
    return angle;

}

double CalcTriArea( point* p1, point* p2, point* p3){

    double area= 0.0;
    area = ( p1->x * (p2->y - p3->y) + p2->x * (p3->y - p1->y) + p3->x * (p1->y - p2->y) ) / 2 ;
    area = sqrt( area*area);
    return area;
}

double CalcLinePointY( double grad, double konst, double x ){

    double y = -1e10;
    y = grad * x + konst;
    return y;

}

int CalcSgn( double val){

    int sgn = 0;
    if( val < 0 ){ sgn = -1; }
    else{ sgn = 1; }
    return sgn;

}

void CalcIntersectPoints( vector<point>* vec, double grad, double konst, double rad, double centX, double centY){

    double x1= 1, x2=101;
    double y1=0.0, y2=0.0;

    if(rad<0){ //dirty fudge for vertical lines
        rad = rad*-1;
        y1=1; y2=101;
        x1=konst; x2=konst;
    }
    else{
        y1=CalcLinePointY( grad, konst, x1);
        y2= CalcLinePointY( grad, konst, x2);
    }

    x1=x1-centX; x2=x2-centX;
    y1=y1-centY; y2=y2-centY;

    double dx = x2-x1, dy = y2-y1;
    double dr= sqrt( dx*dx + dy*dy);

    double det= x1*y2 - x2*y1;
    double inc = rad*rad*dr*dr - det*det;

    /*
    cout<<" P1: "<<x1<<","<<y1<<"\t P2: "<<x2<<","<<y2<<endl;
    cout<<" dx: "<<dx<<"\t dy: "<<dy<<"\t dr: "<<dr<<endl;
    cout<<" det: "<<det<<"\t inc: "<<inc<<"\t sgn(dy): "<<CalcSgn(dy)<<endl;
    */

    if(inc >= 0){
        double intX = -1, intY=-1;

        intX = ( det*dy + CalcSgn(dy)*dx * sqrt(rad*rad*dr*dr - det*det) ) / (dr*dr) ;
        intY = ( -det*dx + sqrt(dy*dy) * sqrt(rad*rad*dr*dr - det*det) ) / (dr*dr) ;
        intX = intX + centX;
        intY = intY + centY;
        //cout<<"1st points intX: "<<intX<<"\t intY: "<<intY<<endl;
        point p1;
        SetPoint(&p1, intX, intY, 0);
        vec->push_back(p1);

        if( inc >0 ){
            intX = -1; intY=-1;
            intX = ( det*dy - CalcSgn(dy)*dx * sqrt(rad*rad*dr*dr - det*det) ) / (dr*dr) ;
            intY = ( -det*dx - sqrt(dy*dy) * sqrt(rad*rad*dr*dr - det*det) ) / (dr*dr) ;
            intX = intX + centX;
            intY = intY + centY;
            //cout<<"2nd points intX: "<<intX<<"\t intY: "<<intY<<endl;
            point p2;
            SetPoint(&p2, intX, intY, 0);
            vec->push_back(p2);
        }

    }
}

double CalcIntersectProp( double rad, double ang){

    double prop= 0.0;
    prop = CalcSecArea(rad, ang)/(PI*rad*rad);
    return prop;

}

int CalcClusterSize(double q1, double q2, double q3, double q4, double THL){

    int cluSize=0;
    if(q1>THL){ cluSize++; }
    if(q2>THL){ cluSize++; }
    if(q3>THL){ cluSize++; }
    if(q4>THL){ cluSize++; }
    return cluSize;
}


double CalcQuadrant( double rad, double cX, double cY, point* p1, point* p2, point* corner){

    //cout<<"*** quadrant ***"<<endl;
    //adjust for non-zero - centre
    point tp1;
    tp1.x=p1->x; tp1.y=p1->y;
    TranslatePoint( &tp1, cX, cY );
    point tp2;
    tp2.x=p2->x; tp2.y=p2->y;
    TranslatePoint( &tp2, cX, cY );
    double angle=CalcSecAngle( rad, &tp1, &tp2 );
    //cout<<"angle: "<<angle<<endl;

    double secArea = CalcSecArea( rad,  angle );
    //cout<<"secArea: "<<secArea<<"\t proportion: "<<secArea/(PI*rad*rad)<<endl;
    double triArea= CalcTriArea( corner, p1, p2);
    //cout<<"triArea: "<<triArea<<"\t proportion: "<<triArea/(PI*rad*rad)<<endl;

    return secArea+triArea;
}


////////////////////
// main
////////////////////

int main(int argc,char** argv) {
    //MSGN(0,"Beginning in section main");

    int minArgs=3;

    vector<point> myVec;
    double myRad=1;
    //tests
    //1. quarter circle
    cout<<"\n*** Test 1"<<endl;
    cout<<"quarter: "<< CalcSegArea( 1, 90)<<",\t pi/4: "<<PI/4<<endl;
    //2. Circle area from chords
    cout<<"\n*** Test 2"<<endl;
    cout<<"quarter chord length: "<<CalcChordLength( myRad, 90)<<endl;
    cout<<"--> quarter section: "<<CalcSecArea( myRad, 90)<<endl;
    cout<<"--> central rectangle: "<<CalcRecArea( CalcChordLength( myRad, 90), CalcChordLength( myRad, 90) )<<endl;
    cout<<"Total circle area: "<< 4*CalcSecArea( myRad, 90) + CalcRecArea( CalcChordLength( myRad, 90), CalcChordLength( myRad, 90) )<<",\t check: "<<PI*myRad*myRad<<endl;
    //3. Line through circle centre=0,0
    cout<<"\n*** Test 3"<<endl;
    CalcIntersectPoints(&myVec, 1, 0, myRad, 0, 0);
    SpitPointVec(&myVec);
    myVec.clear();
    //4. Line through circle centre=1,2
    cout<<"\n*** Test 4"<<endl;
    //CalcIntersectPoints(&myVec, 1, 1, myRad, 1, 2);
    CalcIntersectPoints(&myVec, 0, 1.5, myRad, 1, 2);
    SpitPointVec(&myVec);
    myVec.clear();
    //5. Proportion of area in section from chord through circle centre, centred 1,2
    cout<<"\n*** Test 5"<<endl;
    CalcIntersectPoints(&myVec, 0, 1.5, myRad, 1, 2);
    SpitPointVec(&myVec);
    cout<<"angle: "<<CalcSecAngle(myRad, &myVec.at(0),&myVec.at(1))<<endl;
    cout<<"proportion: "<<CalcIntersectProp( myRad, CalcSecAngle(myRad, &myVec.at(0),&myVec.at(1)) ) <<endl;
    myVec.clear();
    //6. Sweep circle across horizontal line
    cout<<"\n*** Test 6"<<endl;
    double myCentX=0.0, myCentY=0.0;
    for( int dy=1; dy<20; dy++){
        myCentY=(10.0-dy)/2;
        CalcIntersectPoints(&myVec, 0, 2, 1, myCentX, myCentY );
        if(myVec.size()==1){ cout<<"centre: "<<myCentX<<","<<myCentY<<"\t tangent"<<endl; }
        else if(myVec.size()<2){ cout<<"centre: "<<myCentX<<","<<myCentY<<"\t no contact"<<endl; }
        else{
            cout<<"centre: "<<myCentX<<","<<myCentY<<"\t prop: "<<CalcIntersectProp( myRad, CalcSecAngle(myRad, &myVec.at(0),&myVec.at(1)) )<<endl;
            cout<<"angle: "<<CalcSecAngle(1, &myVec.at(0),&myVec.at(1))<<endl;
        }
        myVec.clear();
    }
    //7. single boundary pixel plot
    cout<<"\n*** Test 7"<<endl;

    TFile* myFile = new TFile("section.root","RECREATE","section.root",1);

    TH2D* sing = new TH2D("singleEdge", "single edge sharing", 80, 0, 4, 80, 0, 4);

    //line parameters
    double lGrad= 0, lKonst=2.0;
    //circle parameters
    double cRad= 1.0;

    for(int i=11; i<70; i++){
        for(int j=1; j<80; j++){
            double cX=0.05*i, cY=0.05*j;
            CalcIntersectPoints(&myVec, lGrad, lKonst, cRad, cX, cY );
            cout<<"centre: "<<cX<<","<<cY<<"\t vecSize: "<<myVec.size()<<endl;
            if(myVec.size()==1){ sing->Fill(cX, cY, -1); }
            else if(myVec.size()<2){ sing->Fill(cX, cY, 0); }
            else{
                double prop=CalcIntersectProp( cRad, CalcSecAngle(cRad, &myVec.at(0),&myVec.at(1)) );
                sing->Fill( cX, cY, prop );
                cout<<"centre: "<<cX<<","<<cY<<"\t vecSize: "<<myVec.size()<<endl;
            }
            myVec.clear();
        }
    }
    cout<<"beyond loop"<<endl;
    myFile->cd();
    sing->Write();
    myFile->Close();
    cout<<"shut!"<<endl;
    //delete sing;
    //delete myFile;

    //8. corner boundary proportion
    cout<<"\n*** Test 8"<<endl;

    vector<point> myVecH;
    vector<point> myVecV;
    myCentX=1.0, myCentY=1.0, myRad=1;
    double myVert=1.5; double myHorz=1.5;

    point corn;
    corn.x=myHorz; corn.y=myVert;

    CalcIntersectPoints(&myVecH, 0, myHorz, myRad, myCentX, myCentY );
    SpitPointVec(&myVecH);
    cout<<"proportion: "<<CalcIntersectProp( 1, CalcSecAngle(myRad, &myVecH.at(0),&myVecH.at(1)) ) <<endl;
    //get left & right points
    point hl; point hr;
    if(  (myCentX - myVecH.at(0).x) >= 0){ hl = myVecH.at(0); hr = myVecH.at(1); }
    else{ hl = myVecH.at(1); hr = myVecH.at(0); }

    CalcIntersectPoints(&myVecV, 0, myVert, -myRad, myCentX, myCentY );
    SpitPointVec(&myVecV);
    cout<<"proportion: "<<CalcIntersectProp( 1, CalcSecAngle(1, &myVecV.at(0),&myVecV.at(1)) ) <<endl;
    //get lower & upper points
    point vb; point vt;
    if(  (myCentY - myVecV.at(0).y) >= 0){ vb = myVecV.at(0); vt = myVecV.at(1); }
    else{ vb = myVecV.at(1); vt = myVecV.at(0); }

    cout<<"hl: "; SpitPoint(&hl); cout<<"\t hr: "; SpitPoint(&hr); cout<<endl;
    cout<<"vt: "; SpitPoint(&vt); cout<<"\t vb: "; SpitPoint(&vb); cout<<endl;

    //quadrant 3
    double Aq3=CalcQuadrant(myRad, myCentX, myCentY, &hl, &vb, &corn);
    //quadrant 4
    double Aq4=CalcQuadrant(myRad, myCentX, myCentY, &hr, &vb, &corn);
    //quadrant 1
    double Aq1=CalcQuadrant(myRad, myCentX, myCentY, &hl, &vt, &corn);
    //quadrant 2
    double Aq2=CalcQuadrant(myRad, myCentX, myCentY, &hr, &vt, &corn);

    double totalArea = Aq1 + Aq2 + Aq3 + Aq4 ;
    cout<<"totalArea: "<<totalArea<<"\t totalProportion: "<<totalArea/(PI*myRad*myRad)<<endl;

    //9. corner boundary sweeps
    cout<<"\n*** Test 9"<<endl;

    myFile = new TFile("section.root","UPDATE","section.root",1);

    int nBins=201;
    double lo=0.0, hi=4.0;

    TH2D* cornerQ1 = new TH2D("cornerQ1", "corner sweep for Q1 (top left)", nBins, lo, hi, nBins, lo, hi);
    TH2D* cornerQ2 = new TH2D("cornerQ2", "corner sweep for Q2 (top right)", nBins, lo, hi, nBins, lo, hi);
    TH2D* cornerQ3 = new TH2D("cornerQ3", "corner sweep for Q3 (bottom left)",  nBins, lo, hi, nBins, lo, hi);
    TH2D* cornerQ4 = new TH2D("cornerQ4", "corner sweep for Q4 (bottom right)",  nBins, lo, hi, nBins, lo, hi);
    TH2D* shareMap = new TH2D("shareMap", "0=none, 1=vert, 2=horz, 3=v*h, 4=corner",  nBins, lo, hi, nBins, lo, hi);
    TH2D* clusterSize_0p0 = new TH2D("clusterSize_0p0", "cluster size per cloud centre (THL=0.001)",  nBins, lo, hi, nBins, lo, hi);
    TH2D* clusterSize_0p05 = new TH2D("clusterSize_0p05", "cluster size per cloud centre (THL=0.05)",  nBins, lo, hi, nBins, lo, hi);
    TH2D* clusterSize_0p1 = new TH2D("clusterSize_0p1", "cluster size per cloud centre (THL=0.1)",  nBins, lo, hi, nBins, lo, hi);
    TH2D* clusterSize_0p15 = new TH2D("clusterSize_0p15", "cluster size per cloud centre (THL=0.15)",  nBins, lo, hi, nBins, lo, hi);
    TH2D* clusterSize_0p2 = new TH2D("clusterSize_0p2", "cluster size per cloud centre (THL=0.2)",  nBins, lo, hi, nBins, lo, hi);
    TH2D* clusterSize_0p25 = new TH2D("clusterSize_0p25", "cluster size per cloud centre (THL=0.25)",  nBins, lo, hi, nBins, lo, hi);
    TH2D* clusterSize_0p3 = new TH2D("clusterSize_0p3", "cluster size per cloud centre (THL=0.3)",  nBins, lo, hi, nBins, lo, hi);
    TH2D* clusterSize_0p333 = new TH2D("clusterSize_0p333", "cluster size per cloud centre (THL=third)",  nBins, lo, hi, nBins, lo, hi);
    TH2D* clusterSize_0p4 = new TH2D("clusterSize_0p4", "cluster size per cloud centre (THL=0.4)",  nBins, lo, hi, nBins, lo, hi);
    TH2D* clusterSize_0p5 = new TH2D("clusterSize_0p5", "cluster size per cloud centre (THL=0.5)",  nBins, lo, hi, nBins, lo, hi);
    TH2D* clusterSize_0p75 = new TH2D("clusterSize_0p75", "cluster size per cloud centre (THL=0.75)",  nBins, lo, hi, nBins, lo, hi);
    TH2D* clusterSize_0p99 = new TH2D("clusterSize_0p99", "cluster size per cloud centre (THL=0.99)",  nBins, lo, hi, nBins, lo, hi);

    vector<point> vecH;
    vector<point> vecV;

    //line parameters
    double hGrad= 0, hKonst=2.0; //horizontal
    double vGrad= 0, vKonst=3.0; //Vertical
    //circle parameters
     cRad= 1.0;

    point corner;
    corner.x=vKonst; corner.y=hKonst;

    bool eject=false;
    vector< vector<bool> > founds;
    for(int v=0;v<25;v++){
        vector<bool> vTemp;
        vTemp.push_back(false); vTemp.push_back(false); vTemp.push_back(false);
        founds.push_back(vTemp);
    }
    vector< vector<double> > shares;
    for(int v=0;v<25;v++){
        vector<double> vTemp;
        vTemp.push_back(0.0); vTemp.push_back(0.0); vTemp.push_back(0.0);
        shares.push_back(vTemp);
    }
    vector< double > THLs;
    THLs.push_back(0.001);
    for(int v=1;v<25;v++){ THLs.push_back(v*0.01); }


    for(int i=1; i<201; i++){
        if(eject){ break; }
        for(int j=1; j<201; j++){

            double contQ1=0.0, contQ2=0.0, contQ3=0.0, contQ4=0.0;
            double cX=0.02*i, cY=0.02*j; int type=-1;
            //double cX=(hi-lo)*i/nBins, cY=(hi-lo)*j/nBins; int type=-1;
            cout<<"centre: "<<cX<<","<<cY<<" ("<<i<<","<<j<<")"<<endl;
            shareMap->Fill(cX, cY, -5);

            //if(cX>2.3 && cY> 1.3){ eject=true; break; }

            bool shareH= false, shareV=false, shareEdge=false;
            //check what sort of sharing
            if( (corner.x > (cX-cRad)) && (corner.x < (cX+cRad)) ){ shareH = true; }//horizontal sharing
            if( (corner.y > (cY-cRad)) && (corner.y < (cY+cRad)) ){ shareV = true; }//vertical sharing
            if( sqrt ( (corner.x - cX)*(corner.x - cX) + (corner.y - cY)*(corner.y - cY) ) <  cRad ){ shareEdge = true; }//vertical sharing
            //cout<<"logic(h,v,e): "<<shareH<<","<<shareV<<","<<shareEdge<<"... "<<sqrt ( (corner.x - cX)*(corner.x - cX) + (corner.y - cY)*(corner.y - cY) )<<endl;

            //avoid far sharing beyond edge regions
            if( cX>=(corner.x+cRad) ){ shareV=false; }
            if( cY>=(corner.y+cRad) ){ shareH=false; }
            //if( cX>(corner.x) &&  cY>(corner.y) && sqrt( (corner.x - cX)*(corner.x - cX) + (corner.y - cY)*(corner.y - cY) ) >  cRad ){ shareV=false; shareH=false; }

            if(!shareH && !shareV){ // no sharing
                //cout<<"no sharing"<<endl; type=0;
                type=0;
                contQ1=0; contQ2=0; contQ4=0;
                if(cX<corner.x && cY<corner.y){ contQ3=1.0; }
                else{ contQ3=0; }
            }

            if(shareH && !shareV && !shareEdge){ //horizontal sharing only
                //cout<<"horizontal only"<<endl; type=2;
                type=2;

                CalcIntersectPoints(&vecH, vGrad, vKonst, -cRad, cX, cY );
                //cout<<"H vecSize: "<<vecH.size()<<endl;
                //SpitPointVec(&myVecH);

                if(vecH.size()==1){ contQ3=-1; contQ4=-1; }
                else if(vecH.size()<1){ contQ3=0; contQ4=0; }
                else{
                    double prop=CalcIntersectProp( cRad, CalcSecAngle(cRad, &vecH.at(0),&vecH.at(1)) );
                    if(cX<corner.x){ contQ3=1-prop; contQ4=prop; }
                    else{ contQ3=prop; contQ4=1-prop; }
                    //cout<<"centre: "<<cX<<","<<cY<<"\t vecSize: "<<vecH.size()<<endl;
                }
                vecH.clear();
            }

            if(shareV && !shareH && !shareEdge){ //vertical sharing only
                //cout<<"vertical only"<<endl; type=1;
                type=1;

                CalcIntersectPoints(&vecV, hGrad, hKonst, cRad, cX, cY );
                //cout<<"V vecSize: "<<vecV.size()<<endl;
                //SpitPointVec(&myVecH);

                if(vecV.size()==1){ contQ3=-1; contQ1=-1; }
                else if(vecV.size()<1){ contQ3=0; contQ1=0; }
                else{
                    double prop=CalcIntersectProp( cRad, CalcSecAngle(cRad, &vecV.at(0),&vecV.at(1)) );
                    if(cY<corner.y){ contQ3=1-prop; contQ1=prop; }
                    else{ contQ3=prop; contQ1=1-prop; }
                    //cout<<"centre: "<<cX<<","<<cY<<"\t vecSize: "<<vecV.size()<<endl;
                }
                vecV.clear();
            }

            if(shareV && shareH && !shareEdge){ //both vertical and horizontal
                //cout<<"both vertical & horizontal"<<endl;
                type=3;

                double above=0.0, below=0.0, left=0.0, right=0.0;
                CalcIntersectPoints(&vecV, hGrad, hKonst, cRad, cX, cY );
                //cout<<"V vecSize: "<<vecV.size()<<endl;
                //SpitPointVec(&myVecH);

                if(vecV.size()==1){ contQ3=-1; contQ1=-1; }
                else if(vecV.size()<1){ contQ3=0; contQ1=0; }
                else{
                    double prop=CalcIntersectProp( cRad, CalcSecAngle(cRad, &vecV.at(0),&vecV.at(1)) );
                    if(cY<corner.y){ contQ1=prop; above=prop;  }
                    else{ contQ1=1-prop; above=1-prop;  }

                    //cout<<"centre: "<<cX<<","<<cY<<"\t vecSize: "<<vecV.size()<<endl;
                }
                vecV.clear();

                CalcIntersectPoints(&vecH, vGrad, vKonst, -cRad, cX, cY );
                //cout<<"H vecSize: "<<vecH.size()<<endl;
                //SpitPointVec(&myVecH);

                if(vecH.size()==1){ contQ3=-1; contQ4=-1; }
                else if(vecH.size()<1){ contQ3=0; contQ4=0; }
                else{
                    double prop=CalcIntersectProp( cRad, CalcSecAngle(cRad, &vecH.at(0),&vecH.at(1)) );
                    if(cX<corner.x){ contQ4=prop; right=prop;  }
                    else{ contQ4=1-prop; right=1-prop; }
                    //cout<<"centre: "<<cX<<","<<cY<<"\t vecSize: "<<vecH.size()<<endl;
                }
                vecH.clear();

                if(cX<corner.x && cY<corner.y){ contQ3=1-above-right; contQ1=above; contQ2=0; contQ4=right; }
                if(cX>corner.x && cY<corner.y){ contQ3=1-right; contQ1=0.0; contQ2=above; contQ4=1-(1-right)-above; }
                if(cX<corner.x && cY>corner.y){ contQ3=1-above; contQ1=1-(1-above)-right; contQ2=right; contQ4=0.0; }
                if(cX>corner.x && cY>corner.y){ contQ3=0.0; contQ1=1-right; contQ2=1-(1-above)-(1-right); contQ4=1-above; }

            }

            if(shareEdge){ //corner
                //cout<<"corner sharing"<<endl;
                type=4;

                bool stop=false;

                //horizontal line first
                CalcIntersectPoints(&vecH, hGrad, hKonst, cRad, cX, cY );
                //SpitPointVec(&myVecH);
                point hl; point hr; // left & right
                //cout<<"H vecSize: "<<vecH.size()<<endl;
                if(vecH.size()>1){
                    if(  (cX - vecH.at(0).x) >= 0){ hl = vecH.at(0); hr = vecH.at(1); }
                    else{ hl = vecH.at(1); hr = vecH.at(0); }
                }
                else if(vecH.size()==1){ //tangent
                    hl = vecH.at(0); hr = vecH.at(0);
                    contQ3=-1; contQ1=-1;
                }
                else{ stop=true; cout<<"no horizontal intersection found"<<endl; }

                CalcIntersectPoints(&vecV, vGrad, vKonst, -cRad, cX, cY );
                //SpitPointVec(&myVecV);
                point vb; point vt; // higher and lower
                //cout<<"V vecSize: "<<vecV.size()<<endl;
                if(vecV.size()>1 ){
                    if(  (cY - vecV.at(0).y) >= 0){ vb = vecV.at(0); vt = vecV.at(1); }
                    else{ vb = vecV.at(1); vt = vecV.at(0); }
                }
                else if(vecV.size()==1){ //tangent
                    vb = vecV.at(0); vt = vecV.at(0);
                    contQ3=-1; contQ4=-1;
                }
                else{ stop=true; cout<<"no vertical intersection found"<<endl; }

                if(!stop){ //if two points for each intersection
                    //cout<<"hl: "; SpitPoint(&hl); cout<<"\t hr: "; SpitPoint(&hr); cout<<endl;
                    //cout<<"vt: "; SpitPoint(&vt); cout<<"\t vb: "; SpitPoint(&vb); cout<<endl;

                    //quadrant 3
                    double Aq3=CalcQuadrant(myRad, myCentX, myCentY, &hl, &vb, &corner);
                    contQ3=Aq3/(PI*cRad*cRad);
                    //quadrant 4
                    double Aq4=CalcQuadrant(myRad, myCentX, myCentY, &hr, &vb, &corner);
                    contQ4=Aq4/(PI*cRad*cRad);
                    //quadrant 1
                    double Aq1=CalcQuadrant(myRad, myCentX, myCentY, &hl, &vt, &corner);
                    contQ1=Aq1/(PI*cRad*cRad);
                    //quadrant 2
                    double Aq2=CalcQuadrant(myRad, myCentX, myCentY, &hr, &vt, &corner);
                    contQ2=Aq2/(PI*cRad*cRad);

                    //cout<<"totalArea: "<<Aq1+Aq2+Aq3+Aq4<<"\t totalProportion: "<<(Aq1+Aq2+Aq3+Aq4)/(PI*cRad*cRad)<<endl;
                }
                vecH.clear();
                vecV.clear();
            }
            cornerQ1->Fill( cX, cY, contQ1);
            cornerQ2->Fill( cX, cY, contQ2);
            cornerQ3->Fill( cX, cY, contQ3);
            cornerQ4->Fill( cX, cY, contQ4);
            shareMap->Fill(cX, cY, type+5);

            if(contQ3<0){
                cout<<" *** -ve content Q3 ***"<<endl;
                cout<<" *** Q1: "<<contQ1<<", Q2: "<<contQ2<<", Q3: "<<contQ3<<", Q4: "<<contQ4<<" ***"<<endl;
                cout<<"sharing type: "<<type<<endl;

            }

            for(int v=0; v<25; v++){

                double cS=CalcClusterSize(contQ1,contQ2,contQ3,contQ4,THLs.at(v));
                if(cS==2 && founds.at(v).at(0)==false){
                    founds.at(v).at(0)=true;
                    shares.at(v).at(0)=corner.y-cY;
                }
                if(cS==3 && founds.at(v).at(1)==false){
                    founds.at(v).at(1)=true;
                    shares.at(v).at(1)=sqrt((corner.x-cX)*(corner.x-cX)+(corner.y-cY)*(corner.y-cY));
                }
                if(cS==4 && founds.at(v).at(2)==false){
                    founds.at(v).at(2)=true;
                    shares.at(v).at(2)=corner.x-cX;
                }
            }

            clusterSize_0p0->Fill( cX, cY, CalcClusterSize(contQ1,contQ2,contQ3,contQ4,0.001));
            clusterSize_0p0->SetAxisRange(0.0,4.0,"Z");
            clusterSize_0p05->Fill( cX, cY, CalcClusterSize(contQ1,contQ2,contQ3,contQ4,0.05));
            clusterSize_0p05->SetAxisRange(0.0,4.0,"Z");
            clusterSize_0p1->Fill( cX, cY, CalcClusterSize(contQ1,contQ2,contQ3,contQ4,0.1));
            clusterSize_0p1->SetAxisRange(0.0,4.0,"Z");
            clusterSize_0p15->Fill( cX, cY, CalcClusterSize(contQ1,contQ2,contQ3,contQ4,0.15));
            clusterSize_0p15->SetAxisRange(0.0,4.0,"Z");
            clusterSize_0p2->Fill( cX, cY, CalcClusterSize(contQ1,contQ2,contQ3,contQ4,0.2));
            clusterSize_0p2->SetAxisRange(0.0,4.0,"Z");
            clusterSize_0p25->Fill( cX, cY, CalcClusterSize(contQ1,contQ2,contQ3,contQ4,0.25));
            clusterSize_0p25->SetAxisRange(0.0,4.0,"Z");
            clusterSize_0p3->Fill( cX, cY, CalcClusterSize(contQ1,contQ2,contQ3,contQ4,0.3));
            clusterSize_0p3->SetAxisRange(0.0,4.0,"Z");
            clusterSize_0p333->Fill( cX, cY, CalcClusterSize(contQ1,contQ2,contQ3,contQ4,1.0/3));
            clusterSize_0p333->SetAxisRange(0.0,4.0,"Z");
            clusterSize_0p4->Fill( cX, cY, CalcClusterSize(contQ1,contQ2,contQ3,contQ4,0.4));
            clusterSize_0p4->SetAxisRange(0.0,4.0,"Z");
            clusterSize_0p5->Fill( cX, cY, CalcClusterSize(contQ1,contQ2,contQ3,contQ4,0.5));
            clusterSize_0p5->SetAxisRange(0.0,4.0,"Z");
            clusterSize_0p75->Fill( cX, cY, CalcClusterSize(contQ1,contQ2,contQ3,contQ4,0.75));
            clusterSize_0p75->SetAxisRange(0.0,4.0,"Z");
            clusterSize_0p99->Fill( cX, cY, CalcClusterSize(contQ1,contQ2,contQ3,contQ4,0.99));
            clusterSize_0p99->SetAxisRange(0.0,4.0,"Z");

            /*if( type < 0 ){ cout<<" *** no status selected ***"<<endl; }
            else{ cout<<"sharing type: "<<type<<endl; }*/
        }
    }

    cout<<"beyond loop"<<endl;

    for(int v=0; v<25; v++){
        cout<<"THL:\t"<<THLs.at(v)<<"\tshare2: "<<shares.at(v).at(0)<<"\tshare3: "<<shares.at(v).at(1)<<"\tshare4: "<<shares.at(v).at(2)<<endl;
    }

    myFile->cd();
    cornerQ1->Write();
    cornerQ2->Write();
    cornerQ3->Write();
    cornerQ4->Write();
    shareMap->Write();
    clusterSize_0p0->Write();
    clusterSize_0p05->Write();
    clusterSize_0p1->Write();
    clusterSize_0p15->Write();
    clusterSize_0p2->Write();
    clusterSize_0p25->Write();
    clusterSize_0p3->Write();
    clusterSize_0p333->Write();
    clusterSize_0p4->Write();
    clusterSize_0p5->Write();
    clusterSize_0p75->Write();
    clusterSize_0p99->Write();
    myFile->Close();
    cout<<"shut!"<<endl;
    //delete sing;
    //delete myFile;

    cout<<"all done"<<endl;
    //MSGN(0,"Finished in section main");
    return 0;
}
