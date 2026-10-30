<?php
include_once 'db.php';

$db = new DB();
$assignments = $db->get_assignments();

?>

<html lang="en">
<head>
    <title>Gugul Classroom</title>
</head>
<body>
<h2>Assignments</h2>
<a href="/create_assignment">Create an assignment</a>
<ul>
    <?php foreach ($assignments as $assignment) { ?>
        <li>
            <a href="/assignment?id=<?php echo $assignment['id'] ?>"><?php echo htmlentities($assignment['name']) ?></a>
        </li>
    <?php } ?>
</ul>
</body>
</html>
