
# Local Chatbot

This is a locally hosted chatbot designed to run offline on your device. It leverages the powerful Phi-3 Large Language Model (LLM) to provide intelligent and conversational interactions. The chatbot also supports other LLMs such as LLaMA 3 and Mirage, allowing you to choose the model that best fits your needs
## Setup Ollama

To get started with Ollama, follow these steps:

**Download Ollama**

[Click here](https://ollama.com/) to download Ollama for your suitable device.

**Pull the LLM**

Once Ollama is installed, open your terminal and use the following commands to pull and run the models:

```bash
    ollama pull <model_name>
```
```bash
    ollama run <model_name>
```
   - **LLaMA 3** (Most powerful. Recommended if your device can handle it):
   
     

   - **Phi 3**:
   
     

   - **Gemma** (Recommended for low-end devices):

     

   - **Gemma 2B** (For low-end devices needing a more compact model):
   

### Notes

- **Model Selection**: Choose the model based on your device's capabilities. LLaMA 3 is the most powerful but requires more resources. Gemma and Gemma 2B are suitable for devices with lower specifications.
- **Terminal Commands**: Ensure you have Ollama correctly installed and accessible from your terminal before running these commands.

By following these steps, you can effectively set up and use Ollama with the appropriate model for your device.

## Run Locally

To run this project locally, you will need to have the following dependencies installed:

- **Conda** (either Anaconda or Miniconda)

Follow these steps to set up the project on your local machine:

#### Clone the Project

First, clone the project repository and navigate into the project folder.
- Using SSH:

```bash
git clone git@github.com:Abhinav-gh/Local-phi3-Chatbot.git
cd Local-phi3-Chatbot
```
#### Setup the Conda Environment
Create a Conda environment named **ownbot** using the provided env.yml file.
```bash
  conda env create -f env.yml
```
#### Activate the Environment
Activate the newly created environment:
```bash
  conda activate ownbot
```
[ x ] Setup complete
#### Additional Steps
- **Verify Environment Activation:** Ensure that the Conda environment is activated by checking the command prompt. It should display (ownbot) at the beginning.
- **Check Installed Packages:** Optionally, verify that the necessary packages are installed by running:
```bash
conda list
```
This should display a list of all installed packages within the environment.
### Run!
There are 2 versions of the chatbot. One is terminal based. Other is web based. 
- Terminal based chatbot:
```bash
python ./chatTerminal.py
```
- Web based chatbot:
```bash
streamlit run ./chatweb.py
```
#### TroubleShooting
- Dependency Conflicts: If there are conflicts with existing packages, try updating Conda and using the `--update-deps` flag:
```bash
conda env create -f env.yml --update-deps
```
- Activation Problems: If the environment doesn't activate, make sure that Conda is correctly installed and added to your system's PATH.




## Authors

- [@Abhinav-gh](https://www.github.com/Abhinav-gh)

