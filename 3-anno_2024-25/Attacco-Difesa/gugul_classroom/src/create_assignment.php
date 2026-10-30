<?php
include_once 'db.php';

$db = new DB();

if (count($_POST)) {
    if (count($_POST['answer']) !== count($_POST['question'])) {
        die('Invalid question/answer count!');
    }

    $assignment = $db->create_assignment($_POST['name'], $_POST['reward']);
    if (!$assignment) {
        die('Cannot create assignment');
    }

    for ($i = 0; $i < count($_POST['answer']); $i++) {
        if (!$db->create_task($assignment['id'], $_POST['question'][$i], $_POST['answer'][$i])) {
            die('Cannot create task');
        }
    }

    header('Location: /assignment?id=' . $assignment['id']);
    return;
}

?>

<html lang="en">
<head>
    <title>Create assignment - Gugul Classroom</title>
</head>
<body>
<form method="post">
    <label>
        Name
        <input type="text" name="name">
    </label>
    <br>
    <label>
        Reward
        <input type="text" name="reward">
    </label>
    <br> <br>
    <label>
        Question 1
        <input type="text" name="question[]">
    </label>
    <label>
        Answer 1
        <input type="text" name="answer[]">
    </label>
    <br> <br>
    <label>
        Question 2
        <input type="text" name="question[]">
    </label>
    <label>
        Answer 2
        <input type="text" name="answer[]">
    </label>
    <br> <br>
    <label>
        Question 3
        <input type="text" name="question[]">
    </label>
    <label>
        Answer 3
        <input type="text" name="answer[]">
    </label>
    <br> <br>
    <input type="submit" value="Create">
</form>
</body>
</html>
