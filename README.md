<div align="center">
<!-- Title: -->
  <a href="https://github.com/AlcyonX/GospelBot">
    <img src="bot.png" height="200">
  </a>
  <h1>The <a href="https://github.com/TheAlgorithms/">GospelBot</a> Project</h1>

  <h2>A bot that spreads the Gospel and the Truth through social media. </h2>
</div>

## Features

- **Daily Verse Videos**: Automatically generate and share inspiring short videos featuring Bible verses.
- **Effortless Video Editing**: Create beautiful, professionally styled edits with minimal effort.
- **Seamless YouTube Integration**: Easy and automatic uploading of videos to YouTube.
- **Simplified Token Management**: Generate YouTube API tokens with ease.
- **User-Friendly Setup**: Quick and straightforward installation and configuration.
- **Customizable Settings**: Tailor the bot's behavior and aesthetics to your preferences.
- **Runs on Any Machine**: No need for a powerful computer—even a Raspberry Pi can handle it.

## Getting Started

### Prerequisites

- Python 3.13

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/AlcyonX/GospelBot
    ```

2. Navigate to the GospelBot directory:
    ```bash
    cd GospelBot
    ```

3. Create a virtual environment:
    ```bash
    python -m venv venv
    ```

4. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Configure environment variables:

    - Create a `.env` file at the root of the project.
    - Add your API keys and other necessary configurations as follows:
    ```bash
    PIXABAY_API_KEY = "YOUR_API_KEY"
    ```

6. **Set up YouTube API Client ID**:

    - Go to the [Google Cloud Console](https://console.cloud.google.com/).
    - Create a new project (or select an existing one).
    - Enable the **YouTube Data API v3** for your project.
    - Go to **API & Services > Credentials**, then click **Create Credentials** and select **OAuth 2.0 Client IDs**.
    - Follow the setup steps to configure your OAuth consent screen and create the credentials.
    - Download the `client_secret.json` file from Google Cloud Console.
    - Move the downloaded `client_secret.json` into the `client_id` folder.

7. Run the bot:
    ```bash
    venv/bin/python3 src/gospelbot/__main__.py
    ```

Now you're all set up to run the GospelBot!

## Usage

### Generate a daily verse short with ```--type```

```bash
python3 path/to/__main__.py --type dailyverse
```

### Publish or not with ```--publish```

```bash
python3 path/to/__main__.py --type dailyverse --publish True
```

## Roadmap

- New type of video
- Other social media
- Improve the video quality

## Contribute

## Contributing

We welcome contributions to this project ! To contribute, please follow these steps:

1. **Fork the repository**: 
   - Click on the "Fork" button at the top right of this page to create a personal copy of the repository.

2. **Clone your fork**: 
   - Clone your fork to your local machine using Git:
     ```bash
     git clone https://github.com/yourusername/GospelBot.git
     ```

3. **Create a new branch**:
   - Create a branch for your feature or bug fix:
     ```bash
     git checkout -b my-feature-branch
     ```

4. **Make your changes**:
   - Make the necessary changes or add new features. Ensure your code follows the existing style and structure of the project.

5. **Commit your changes**:
   - After making changes, commit them with a descriptive message:
     ```bash
     git commit -m "Add feature X or fix bug Y"
     ```

6. **Push your changes**:
   - Push your changes to your forked repository:
     ```bash
     git push origin my-feature-branch
     ```

7. **Submit a pull request (PR)**:
   - Go to the original repository and click on "Pull Requests" then "New Pull Request."
   - Select your branch and describe your changes in detail. Make sure your pull request follows our contribution guidelines.
   
8. **Wait for review**:
   - After submitting the PR, a project maintainer will review your changes. If everything is in order, they will merge your contribution!

### Code of Conduct

We are committed to creating a positive, supportive, and respectful environment focused on spreading the gospel message. By participating in this project, you agree to the following principles:

### Our Pledge

As contributors and participants, we pledge to work together to spread the good news of Jesus Christ in a manner that is loving, kind, and respectful.

### Our Standards

We expect all participants to:

- **Honor the Gospel**: Ensure that all contributions align with the message of spreading the gospel.
- **Encourage Respectful Dialogue**: Engage in discussions that promote understanding and peace.
- **Foster Inclusivity**: Treat everyone with kindness and respect, regardless of their background or beliefs.
- **Promote Positive Behavior**: Strive to help others and maintain patience, empathy, and support in all interactions.

### Unacceptable Behavior

The following behaviors are not acceptable:

- Disrespectful or harmful language.
- Promoting hate speech or divisive behavior.

Thank you for contributing to a space that fosters a loving, kind, and respectful environment for sharing the gospel.


## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

The GPL v3 license ensures that you have the freedom to run, modify, and share the software. Any modified version of this project must also be released under the GPL v3 license.

# Donate

If you find this project useful and want to support its development, you can make a donation through PayPal.

### Donate via PayPal

Click the link below to make a donation:

[Donate via PayPal](https://www.paypal.com/donate/?hosted_button_id=7LM83HXWXMBN6)

Your contributions help us continue improving and maintaining this project. Thank you for your support!

## PRAISE THE LORD JESUS CHRIST ✝

