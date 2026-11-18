
async function generateContent() {

    const topic = document.getElementById("topic").value.trim();
    const audience = document.getElementById("audience").value.trim();

    const button = document.getElementById("generateBtn");
    const status = document.getElementById("status");

    if (!topic || !audience) {
        status.innerText = "Please enter both topic and audience.";
        return;
    }

    button.disabled = true;
    button.innerText = "Generating...";
    status.innerText = "Please wait! AI is generating your content.";

    try {

        const response = await fetch("/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                topic: topic,
                audience: audience
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Something went wrong.");
        }

        document.getElementById("content").innerText = data.content;
        document.getElementById("caption").innerText = data.caption;
        document.getElementById("hashtags").innerText = data.hashtags;

        status.innerText = "Content generated successfully!";

    } catch (error) {

        status.innerText = error.message;

    } finally {

        button.disabled = false;
        button.innerText = "✨ Generate AI Content";

    }
}
