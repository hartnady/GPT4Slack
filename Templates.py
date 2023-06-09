HELP_MENU = ' \n>`/gpt your_prompt` will enqueue a *new* request with the GPT service. e.g. `/gpt give me a chocolate cake recipe`'
HELP_MENU += '\n>`/gpt <request-id>` will provide the status of a *previous request* e.g. `/gpt 255`'
HELP_MENU += '\n>`/gpt <request-id> your_next_prompt` will continue a *previous dialogue* e.g. `/gpt 255 give me baking instructions for the cake`'
HELP_MENU += '\n>`/gpt share <request-id> with <slack-user>` will share your request with another user e.g. `/gpt share 255 with firstname.lastname`'
HELP_MENU += '\n>`/gpt list` will list your last 5 request ids'
HELP_MENU += '\nAll GPT responses will be sent in a private message back to the requesting user.'
HELP_MENU += '\nTo post the response publically to the channel where you issued the request, you can click `Post to Channel`.'
HELP_MENU += '\nFor this to work, you must first `/invite @GPT` to the channel'
HELP_MENU += '\nMax prompt length is *3000 characters*'

DISCLAIMER  = "1. Remember to *fact check* any responses generated by GPT or any other generative A.I.\n"
DISCLAIMER += "2. Be aware of the potential *biases and limitations* of the generative AI model you are using, and actively work to mitigate them.\n"
DISCLAIMER += "3. Always *attribute the output* of generative AI to its source, and be transparent about the fact that it was generated using an AI model.\n"
DISCLAIMER += "4. Use generative AI to *augment your own creativity and work*, rather than as a replacement for it.\n"
DISCLAIMER += "5. Regularly *evaluate and reassess the ethical implications* of your use of generative AI, and be willing to adjust your practices accordingly.\n"
DISCLAIMER += "6. *Unethical or dishonest* use of generative AI may lead to *disciplinary action*.\n"

HOME_BLOCK = {
   "type":"home",
   "blocks":[
                { "type":"section", "text":{ "type":"mrkdwn", "text":"Welcome to *GPT for Slack*. Your personal A.I. assistant. This service is powered by OpenAI's GPT 3.5 Turbo Conversational API, and funded by VRP.\nPlease provide feedback to <mailto:mark.hartnady@vrpconsulting.com|Mark Hartnady>." } },
        		{ "type": "header", "text": { "type": "plain_text", "text": "Ethical A.I. Checklist", "emoji": True } },
		        { "type": "divider" },
		        { "type":"section", "text":{ "type":"mrkdwn", "text":DISCLAIMER } },
		        { "type": "header", "text": { "type": "plain_text", "text": "Help", "emoji": True } },
		        { "type": "divider" },
		        { "type":"section", "text":{ "type":"mrkdwn", "text":HELP_MENU } }
        ]
}

RESPONSE_PROMPT_TOO_LONG = {
    "type": "modal", "title": { "type": "plain_text", "text": "GPT Responder" },
    "close": { "type": "plain_text", "text": "Close" },
    "blocks": [
            { "type": "header", "text": { "type": "plain_text", "text": "Oops!", "emoji": True } },
            { "type": "section", "text": { "type": "mrkdwn", "text": "Your prompt (Text/Email Input/Code) was too long. Please try again. Max characters = 3000" } },
        ]
}

RESPONSE_SUCCESS = {
    "type": "modal", "title": { "type": "plain_text", "text": "GPT Responder" },
    "close": { "type": "plain_text", "text": "Close" },
    "blocks": [
            { "type": "header", "text": { "type": "plain_text", "text": "Thank you!", "emoji": True } },
            { "type": "section", "text": { "type": "mrkdwn", "text": "" } },
            { "type": "header", "text": { "type": "plain_text", "text": "Ethical A.I. Checklist", "emoji": True } },
            { "type": "section", "text": { "type": "mrkdwn", "text": DISCLAIMER } }
        ]
}

MAIN_MODAL_DEGRADATION = {
	"type": "modal",
	"title": { "type": "plain_text","text": "GPT Operation Handler" },
	"submit": { "type": "plain_text", "text": "Submit" },
	"close": { "type": "plain_text", "text": "Cancel" },
	"blocks": [
		{ "type": "divider" },
		{ "type": "section", "text": { "type": "mrkdwn", "text": ":red_circle: *NOTICE: GPT is experiencing performance degradation* :red_circle:\nhttps://status.openai.com" } },
		{ "type": "divider" },
		{ "type": "section", "text": { "type": "mrkdwn", "text": "Please select a task and input prompt (*max chars = 3000*):" } },
		{ "type": "input",
		  "label": { "type": "plain_text", "text": "Task", "emoji": True },
		  "element": {
		        "type": "static_select",
		        "placeholder": { "type": "plain_text", "text": "Select an item", "emoji": True },
				"action_id": "INPUT_OPERATION",
				"initial_option": { "text": { "type": "plain_text", "text": "Answer Question", "emoji": True }, "value": "none" },
		        "option_groups": [
					{
						"label": { "type": "plain_text", "text": "General" },
        				"options": [
        				    { "text": { "type": "plain_text", "text": "Answer Question", "emoji": True }, "value": "none" },
        				    { "text": { "type": "plain_text", "text": "Translate to English", "emoji": True }, "value": "translate_en" },
        					{ "text": { "type": "plain_text", "text": "Перевести на русский", "emoji": True }, "value": "translate_ru" },
        					{ "text": { "type": "plain_text", "text": "Przetłumacz na język polski", "emoji": True }, "value": "translate_pl" },
        					{ "text": { "type": "plain_text", "text": "Summarise the text", "emoji": True }, "value": "summarize" },
        					{ "text": { "type": "plain_text", "text": "Fix the grammar", "emoji": True }, "value": "fix-grammar" }
        				]
        			},
        			{
						"label": { "type": "plain_text", "text": "Developer" },
        				"options": [
        					{ "text": { "type": "plain_text", "text": "Add comments to this code", "emoji": True }, "value": "add-comment" },
        					{ "text": { "type": "plain_text", "text": "Fix/debug this code", "emoji": True }, "value": "fix-code" },
        					{ "text": { "type": "plain_text", "text": "Write a unit test for this code", "emoji": True }, "value": "unit-test" },
        					{ "text": { "type": "plain_text", "text": "Convert this text to JSON", "emoji": True }, "value": "convert-json" },
        					{ "text": { "type": "plain_text", "text": "Convert code to Acceptance Criteria (GIVEN/WHEN/THEN)", "emoji": True }, "value": "code2acceptance" }

        				]
        			},
        			{
						"label": { "type": "plain_text", "text": "Quality Assurance" },
        				"options": [
        					{ "text": { "type": "plain_text", "text": "Draw a sequence diagram of this code", "emoji": True }, "value": "sequence" },
        					{ "text": { "type": "plain_text", "text": "Convert requirement to User Story format", "emoji": True }, "value": "user-story" },
        					{ "text": { "type": "plain_text", "text": "Produce Test Steps for this requirement", "emoji": True }, "value": "test-steps" },
        					{ "text": { "type": "plain_text", "text": "Convert requirement to Acceptance Criteria (GIVEN/WHEN/THEN)", "emoji": True }, "value": "acceptance-criteria" },
        					{ "text": { "type": "plain_text", "text": "Convert code to Acceptance Criteria (GIVEN/WHEN/THEN)", "emoji": True }, "value": "code2acceptance" }

        				]
        			},
        			{
						"label": { "type": "plain_text", "text": "Marketing" },
        				"options": [
        				    { "text": { "type": "plain_text", "text": "Analyse text for SEO Keywords", "emoji": True }, "value": "seo" }
        				]
        			},
        			{
						"label": { "type": "plain_text", "text": "Sales" },
        				"options": [
        					{ "text": { "type": "plain_text", "text": "Analyse text to create a proposal outline", "emoji": True }, "value": "proposal" }
        				]
        			},
        			{
						"label": { "type": "plain_text", "text": "Delivery" },
        				"options": [
        					{ "text": { "type": "plain_text", "text": "Analyse text for delivery risks", "emoji": True }, "value": "risks" },
        					{ "text": { "type": "plain_text", "text": "Analyse text to create a workshop agenda", "emoji": True }, "value": "workshop" }
        				]
        			},
        			{
						"label": { "type": "plain_text", "text": "Misc." },
        				"options": [
        					{ "text": { "type": "plain_text", "text": "None - just execute my prompt", "emoji": True }, "value": "none" }
        				]
        			}
				]
			}
		},
		{   "type": "input",
		    "element": { "type": "plain_text_input", "initial_value": "", "multiline": True, "placeholder": { "type": "plain_text", "text": "Enter your prompt here..." }, "action_id": "INPUT_TEXT" },
		    "label": { "type": "plain_text", "text": "Your Prompt" }
		}
	]
}

MAIN_MODAL = {
	"type": "modal",
	"title": { "type": "plain_text","text": "GPT Operation Handler" },
	"submit": { "type": "plain_text", "text": "Submit" },
	"close": { "type": "plain_text", "text": "Cancel" },
	"blocks": [
		{ "type": "section", "text": { "type": "mrkdwn", "text": "Please select a task and input prompt:" } },
		{ "type": "input",
		  "label": { "type": "plain_text", "text": "Task", "emoji": True },
		  "element": {
		        "type": "static_select",
		        "placeholder": { "type": "plain_text", "text": "Select an item", "emoji": True },
				"action_id": "INPUT_OPERATION",
				"initial_option": { "text": { "type": "plain_text", "text": "Answer Question", "emoji": True }, "value": "none" },
		        "option_groups": [
        			{
						"label": { "type": "plain_text", "text": "Marketing" },
        				"options": [
        				    { "text": { "type": "plain_text", "text": "Analyse text for SEO Keywords", "emoji": True }, "value": "seo" }
        				]
        			},
        			{
						"label": { "type": "plain_text", "text": "Sales" },
        				"options": [
        					{ "text": { "type": "plain_text", "text": "Analyse text to create a proposal outline", "emoji": True }, "value": "proposal" }
        				]
        			},
        			{
						"label": { "type": "plain_text", "text": "Delivery" },
        				"options": [
        					{ "text": { "type": "plain_text", "text": "Analyse text for delivery risks", "emoji": True }, "value": "risks" },
        					{ "text": { "type": "plain_text", "text": "Analyse text to create a workshop agenda", "emoji": True }, "value": "workshop" }
        				]
        			},
					{
						"label": { "type": "plain_text", "text": "General" },
        				"options": [
        				    { "text": { "type": "plain_text", "text": "Answer Question", "emoji": True }, "value": "none" },
        				    { "text": { "type": "plain_text", "text": "Translate to English", "emoji": True }, "value": "translate_en" },
        					{ "text": { "type": "plain_text", "text": "Перевести на русский", "emoji": True }, "value": "translate_ru" },
        					{ "text": { "type": "plain_text", "text": "Przetłumacz na język polski", "emoji": True }, "value": "translate_pl" },
        					{ "text": { "type": "plain_text", "text": "Summarise the text", "emoji": True }, "value": "summarize" },
        					{ "text": { "type": "plain_text", "text": "Fix the grammar", "emoji": True }, "value": "fix-grammar" }
        				]
        			},
        			{
						"label": { "type": "plain_text", "text": "Developer" },
        				"options": [
        					{ "text": { "type": "plain_text", "text": "Add comments to this code", "emoji": True }, "value": "add-comment" },
        					{ "text": { "type": "plain_text", "text": "Fix/debug this code", "emoji": True }, "value": "fix-code" },
        					{ "text": { "type": "plain_text", "text": "Write a unit test for this code", "emoji": True }, "value": "unit-test" },
        					{ "text": { "type": "plain_text", "text": "Convert this text to JSON", "emoji": True }, "value": "convert-json" },
        					{ "text": { "type": "plain_text", "text": "Convert code to Acceptance Criteria (GIVEN/WHEN/THEN)", "emoji": True }, "value": "code2acceptance" }

        				]
        			},
        			{
						"label": { "type": "plain_text", "text": "Quality Assurance" },
        				"options": [
        					{ "text": { "type": "plain_text", "text": "Draw a sequence diagram of this code", "emoji": True }, "value": "sequence" },
        					{ "text": { "type": "plain_text", "text": "Convert requirement to User Story format", "emoji": True }, "value": "user-story" },
        					{ "text": { "type": "plain_text", "text": "Produce Test Steps for this requirement", "emoji": True }, "value": "test-steps" },
        					{ "text": { "type": "plain_text", "text": "Convert requirement to Acceptance Criteria (GIVEN/WHEN/THEN)", "emoji": True }, "value": "acceptance-criteria" },
        					{ "text": { "type": "plain_text", "text": "Convert code to Acceptance Criteria (GIVEN/WHEN/THEN)", "emoji": True }, "value": "code2acceptance" }

        				]
        			},
        			{
						"label": { "type": "plain_text", "text": "Misc." },
        				"options": [
        					{ "text": { "type": "plain_text", "text": "None - just execute my prompt", "emoji": True }, "value": "none" }
        				]
        			}
				]
			}
		},
		{   "type": "input",
		    "element": { "type": "plain_text_input", "initial_value": "", "multiline": True, "placeholder": { "type": "plain_text", "text": "Enter your prompt here..." }, "action_id": "INPUT_TEXT" },
		    "label": { "type": "plain_text", "text": "Your Prompt" }
		}
	]
}
