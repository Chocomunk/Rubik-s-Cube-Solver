/*
 * Creates functions to find subsequent movement on the opposite side
 */
struct Move {
	
public:
    Move(int asciiCode);
    static bool isOpposite(Move &m1, Move &m2) {
	  	return (m1.getIndex() == m2.getIndex()) && (m1.isOnLeft() != m2.isOnLeft());
		}
    char getType();
    int getIndex();
    bool isOnLeft();
    
private:
    char moveType;
    int index;
    bool isLeftSide;
};
