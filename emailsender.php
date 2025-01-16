<?php
// Check if the required POST parameters are set
if (isset($_POST['to']) && isset($_POST['subject']) && isset($_POST['body'])) {
    $to = $_POST['to'];
    $subject = $_POST['subject'];
    $body = $_POST['body'];
    $headers = "From: no-reply@example.com\r\n";  // Replace with your desired sender email
    $headers .= "Reply-To: no-reply@example.com\r\n";
    $headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

    // Send the email using PHP's mail function
    if (mail($to, $subject, $body, $headers)) {
        echo "Email sent successfully.";
    } else {
        echo "Failed to send email.";
    }
} else {
    echo "Error: Missing required parameters.";
}
?>
