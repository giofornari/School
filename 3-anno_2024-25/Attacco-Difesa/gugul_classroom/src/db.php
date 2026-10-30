<?php

class DB
{
    private mysqli $db;

    function __construct()
    {
        $this->db = mysqli_connect($_ENV['DB_HOST'], $_ENV['DB_USER'], $_ENV['DB_PASSWD'], $_ENV['DB_NAME']);
    }

    function get_assignments(): false|array
    {
        $res = mysqli_query($this->db, "select id, name, reward from assignments");
        if (!$res)
            return false;

        $list = [];
        while ($row = $res->fetch_assoc()) {
            $list[] = $row;
        }

        return $list;
    }

    function create_assignment($name, $reward): false|array
    {
        $res = mysqli_query($this->db, "insert into assignments (name, reward) values ('" . $name . "', '" . $reward . "')");
        if (!$res)
            return false;

        $assignment_id = mysqli_insert_id($this->db);
        return $this->get_assignment($assignment_id);
    }

    function get_assignment($assignment_id): false|array
    {
        $res = mysqli_query($this->db, "select id, name, reward from assignments where id = " . $assignment_id . " limit 1");
        if (!$res)
            return false;

        return $res->fetch_assoc();
    }

    function create_task($assignment_id, $question, $answer): bool
    {
        $res = mysqli_query($this->db, "insert into tasks (assignment_id, question, answer) values (" . $assignment_id . ", '" . $question . "', '" . $answer . "')");
        if (!$res)
            return false;

        return true;
    }

    function get_tasks($assignment_id): false|array
    {
        $res = mysqli_query($this->db, "select id, question, answer from tasks where assignment_id = " . $assignment_id);
        if (!$res)
            return false;

        $list = [];
        while ($row = $res->fetch_assoc()) {
            $list[] = $row;
        }

        return $list;
    }
}