<!DOCTYPE html>
<html>
<head>
    <title>Results</title>
</head>
<body>

<h2>Candidate Results</h2>

<p>Exam Number: {{ exam_number }}</p>

<table border="1">

<tr>
    <th>Subject</th>
    <th>Grade</th>
</tr>

{% for row in results %}

<tr>
    <td>{{ row[0] }}</td>
    <td>{{ row[1] }}</td>
</tr>

{% endfor %}

</table>

</body>
</html>
