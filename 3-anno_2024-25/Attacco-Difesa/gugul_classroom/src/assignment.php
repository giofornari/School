<?php
include_once 'db.php';

$db = new DB();

$assignment = $db->get_assignment($_GET['id']);
if (!$assignment) {
    die('Invalid assignment');
}

$tasks = $db->get_tasks($assignment['id']);
if (!$tasks) {
    die();
}

if (count($_POST)) {
    for ($i = 0; $i < count($_POST['answer']); $i++) {
        if ($_POST['answer'][$i] !== $tasks[$i]['answer']) {
            die('Wrong answers!');
        }
    }

    echo 'Your reward: ' . $assignment['reward'];
    return;
}

?>

<html lang="en">
<head>
    <title><?php echo htmlentities($assignment['name']) ?> - Gugul Classroom</title>
</head>
<body>
<h1><?php echo htmlentities($assignment['name']) ?></h1>
<form method="post">
    <?php foreach ($tasks as $task) { ?>
        <h3>Question</h3>
        <p><?php echo htmlentities($task['question']) ?></p>
        <label>
            Answer
            <input type="text" name="answer[]">
        </label>
        <br><br>
    <?php } ?>

    <input type="submit" value="Submit">
</form>
</body>
</html>

