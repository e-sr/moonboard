
DROP TABLE IF EXISTS holds;
DROP TABLE IF EXISTS setter;
DROP TABLE IF EXISTS problemMoves;
DROP TABLE IF EXISTS problems;
--
CREATE TABLE holds(
    Position TEXT, 
    Setup TEXT,
    HoldSet TEXT, 
    Hold INTEGER,
    Orientation TEXT,
    PRIMARY KEY (Position,Setup)
    );
--
CREATE TABLE setter
(
    Firstname TEXT,
    Lastname TEXT,
    PRIMARY KEY (Firstname,Lastname)
);
--
CREATE TABLE problems(
    Id INTEGER PRIMARY KEY, 
    Name TEXT , 
    Grade TEXT,
    IsBenchmark INTEGER,
    IsAssessmentProblem INTEGER,
    Method TEXT,
    Firstname TEXT,
    Lastname TEXT,
    FOREIGN KEY (Firstname,Lastname) REFERENCES setter(Firstname,Lastname)
    );
--
CREATE TABLE problemMoves(
    Problem INTEGER,
    Position TEXT,
    Setup TEXT,
    IsStart INTEGER, 
    IsEnd INTEGER, 
    PRIMARY KEY (Problem,Position,Setup),
    FOREIGN KEY (Problem) REFERENCES problems (Id),
    FOREIGN KEY (Position,Setup) REFERENCES holds (Position,Setup)
    );
