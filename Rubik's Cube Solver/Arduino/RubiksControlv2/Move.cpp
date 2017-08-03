#include "Move.h";
char* oppositeboi[] = {"uUvdDe", "lLmrRs", "fFgbBc"};

char Move::getType() {
    return this->moveType;
}

int Move::getIndex(){
	return this->index;
}

bool Move::isOnLeft(){
	return this->isLeftSide;
}

Move::Move(int asciiCode) {
	this->moveType = (char)asciiCode;
	bool isFound;
  int list=0;
  int leftlist;
  int i=0;
  int compIndex;
	while(!isFound && i<3) {
	  while(!isFound && list<6) {
      isFound = this->moveType == oppositeboi[i][list];
      leftlist=list;
      list++;
	  }
  list=0;
  compIndex=i;
  i++;
	}
  this->isLeftSide = (leftlist<3);
  this->index=compIndex;
}
