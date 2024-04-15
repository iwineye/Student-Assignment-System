#USER TABLE
CREATE TABLE User (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);

#ASSIGNMENT TABLE
CREATE TABLE Assignment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    user_id INT NOT NULL,
    user_name VARCHAR(50) NOT NULL,
    subject VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    due_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(id)
);

SELECT * FROM assignments.user;
ALTER TABLE user
#adding column
ADD COLUMN is_superuser BOOLEAN DEFAULT FALSE;
#adding super user access
UPDATE user
SET is_superuser = TRUE
WHERE username = 'TEACHER_01';

