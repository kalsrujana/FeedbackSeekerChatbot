# Feedback Seeker / Opinion Recorder Telegram Bot

The Feedback Seeker (also known as Opinion Recorder) Telegram Bot is a chatbot designed to interact with customers on the [OpinionSeekerBot](https://t.me/OpinionSeekerBot). It focuses on collecting and processing customer feedback based on various events, such as transaction completions, product purchases, or any other interactions.

## Features

The bot excels in the following key features:

- **Feedback Solicitation:** The bot proactively reaches out to customers to request their valuable feedback. It initiates conversations following certain events or triggers, engaging customers to share their opinions.

- **Feedback Classification:** The Opinion Recorder is equipped with sentiment analysis capabilities. It automatically classifies incoming customer messages, determining whether they contain feedback and, if so, categorizing it as positive, negative, or neutral.

- **Personalized Responses:** For each received feedback, the bot generates personalized responses. It addresses customers by name, shows appreciation for their input, and provides relevant follow-up information or assistance.

- **Asynchronous Feedback Recording:** All collected feedback is recorded asynchronously, ensuring that no customer input is lost. The bot securely stores this feedback for further analysis or review.

## Getting Started

1. **Bot Interaction:** To begin using the Opinion Recorder Bot, visit the [OpinionSeekerBot](https://t.me/OpinionSeekerBot) on Telegram.

2. **Engage with the Bot:** Start a conversation or respond to the bot's prompts, sharing your feedback based on recent events.

3. **Receive Personalized Responses:** The bot will acknowledge your feedback, provide additional information, and offer support as needed.

4. **Feedback Processing:** Your messages will be automatically classified based on sentiment and content, ensuring a comprehensive understanding of your input.

5. **Feedback Recording:** Your feedback will be recorded for further analysis, enhancing services and products.

## Workflow design
---
### Feedback solicitation workflow
<p align="center">
  <img src="https://github.com/kalsrujana/FeedbackSeekerChatbot/blob/main/feedback_solicitation.png" width="700" />
</p>

---
### Response generator and Feedback-storing workflow
<p align="center">
  <img src="https://github.com/kalsrujana/FeedbackSeekerChatbot/blob/main/feedbackSeeker_workflow.png" width="700" />
</p>

---
### Detailed Step function graph
<p align="center">
  <img src="https://github.com/kalsrujana/FeedbackSeekerChatbot/blob/main/stepfunctions_graph.png" width="700" />
</p>
