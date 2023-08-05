# Analytics Data

## Public APIs

### Usage Stats
{
    "aggregate_stats": {
        "ambiguous_messages_count": 8, 
        "end_time": 1552118399.0, 
        "messages_count": 94, 
        "session_count": 1, 
        "start_time": 1515715200.0, 
        "successful_responses_count": 77, 
        "unhandled_messages_count": 9
    }, 
    "stats": [
        {
            "ambiguous_messages_count": 0, 
            "end_time": 1519759999.8888888, 
            "messages_count": 0, 
            "session_count": 0, 
            "start_time": 1515715200.0, 
            "successful_responses_count": 0, 
            "unhandled_messages_count": 0
        }, 
        {
            "ambiguous_messages_count": 0, 
            "end_time": 1523804799.7777777, 
            "messages_count": 0, 
            "session_count": 0, 
            "start_time": 1519759999.8888888, 
            "successful_responses_count": 0, 
            "unhandled_messages_count": 0
        }, 
        {
            "ambiguous_messages_count": 0, 
            "end_time": 1527849599.6666667, 
            "messages_count": 0, 
            "session_count": 0, 
            "start_time": 1523804799.7777777, 
            "successful_responses_count": 0, 
            "unhandled_messages_count": 0
        }, 
        {
            "ambiguous_messages_count": 0, 
            "end_time": 1531894399.5555556, 
            "messages_count": 0, 
            "session_count": 0, 
            "start_time": 1527849599.6666667, 
            "successful_responses_count": 0, 
            "unhandled_messages_count": 0
        }, 
        {
            "ambiguous_messages_count": 0, 
            "end_time": 1535939199.4444444, 
            "messages_count": 0, 
            "session_count": 0, 
            "start_time": 1531894399.5555556, 
            "successful_responses_count": 0, 
            "unhandled_messages_count": 0
        }, 
        {
            "ambiguous_messages_count": 0, 
            "end_time": 1539983999.3333333, 
            "messages_count": 0, 
            "session_count": 0, 
            "start_time": 1535939199.4444444, 
            "successful_responses_count": 0, 
            "unhandled_messages_count": 0
        }, 
        {
            "ambiguous_messages_count": 0, 
            "end_time": 1544028799.2222223, 
            "messages_count": 0, 
            "session_count": 0, 
            "start_time": 1539983999.3333333, 
            "successful_responses_count": 0, 
            "unhandled_messages_count": 0
        }, 
        {
            "ambiguous_messages_count": 0, 
            "end_time": 1548073599.1111112, 
            "messages_count": 0, 
            "session_count": 0, 
            "start_time": 1544028799.2222223, 
            "successful_responses_count": 0, 
            "unhandled_messages_count": 0
        }, 
        {
            "ambiguous_messages_count": 8, 
            "end_time": 1552118399.0, 
            "messages_count": 94, 
            "session_count": 1, 
            "start_time": 1548073599.1111112, 
            "successful_responses_count": 77, 
            "unhandled_messages_count": 9
        }
    ]
}

Process finished with exit code 0



## Dashboard APIs

### Result_by_filters

#### Data Dictionary

This particular entry is from a knowledge pack that is present in all virtual assistants training. In this particular case the utterance is hello. This utterance triggered this JSON object entry

````json
{
            "bot": {
                "display_name": "Acme Sales ", 
                "id": 4709
            }, 
            "channel_name": "web", 
            "conversation_uuid": "05e6be529606db217d5ef1aa4f4e7a14", 
            "created_at": 1548304346.0, 
            "id": 2189971, 
            "intent_name": "Greetings", 
            "intent_type": "Knowledge Pack", 
            "node_key": "4", 
            "query_insights": {
                "analyzed_document": "Hello", 
                "bow_normalized_document": "hello", 
                "bow_normalized_document_with_stopwords": "hello", 
                "bow_words": [
                    "hello"
                ],
                "detected_language": "en", 
                "document": "Hello", 
                "domain_ids": [], 
                "entities": [], 
                "featured_normalized_tokens": "hello", 
                "featured_tokens": [
                    "hello"
                ], 
                "featured_tokens_lemma_map": {
                    "hello": "hello"
                }, 
                "id": null, 
                "intent": "", 
                "is_transaction": false, 
                "negation": false, 
                "new_normalized_document": "Hello", 
                "new_normalized_document_query": "Hello", 
                "normalized_document": "hello", 
                "normalized_tokens": "hello", 
                "original_document": "Hello", 
                "original_text": "Hello", 
                "plain_document": "Hello", 
                "pos": [
                    [
                        "hello", 
                        "NN"
                    ]
                ], 
                "raw_document": "Hello", 
                "score": 0, 
                "second_best_result": null, 
                "tone": "Anger"
            }, 
            "score": 1.0, 
            "user": {
                "display_name": "David Gwartney", 
                "id": 25908
            }, 
            "user_query": "Hello"
}
````

#### Chatbot Information

Specific information about the chatbot is contained within the bot JSON object as shown here:

````json
"bot": {
  "display_name": "Acme Sales",
  "id": 4709
}
````

The object contains two fields as follows:

**display_name**

Name of the chatbot from the designer web page

**id**

Unique identifier of the chatbot within the account

**Channel Name**

_Channel_name_ is the messaging service the chatbot is attached to.
Channel name can be various values from facebook to sms. See list
of some of the values that channel name can assume:

- _web_ - Web Browser
- _facebook_ - Facebook Messenger

**Conversation Id**

Unique defines the conversation, conversations are defined from the time the chat window is open until and receives text until idle for two minutes.

**Created At**

Time the message was sent in epoch time

**Id**

Unique identifier of the message

**Intent Name**

Identifies the unique intent triggered

**Intent Type**

Type of the intent can be one of:

- _Domain_ - The intent is from a defined domain
- _Entity_ - The entity is from a defined domain
- _Inline_ - The intent was created directly in the conversational graph
- _Js_ - Custom intent where by JavaScript is used to see if the intent is triggered.

**Node Key**

Node number from the conversation graph

**Query Insights**

_query_insights_ contains multiple values describing the analysis of the query:

````json
"query_insights": {
  "analyzed_document": "Hello", 
  "bow_normalized_document": "hello", 
   "bow_normalized_document_with_stopwords": "hello", 
   "bow_words": [
     "hello"
   ]
}
````

**Analyzed Document**

Document Text

**Bag of Words Normalized Document**

**Bag of Words Normalized Document with Stopwords**

**Bag of Words**

**Confidence Score**

Score is a value between 0 and 1 indicates with which confidence that the intent trigger by the user query.

**Detected Language**

Language detected buy the NLP engine.

**Document**

````json
"document": "Chardonnay"
````

**Domain Ids**

````json
"domain_ids": []
````

**Entities**

````json
"entities": [
                    {
                        "current_value": "chardonnay", 
                        "domain_key": "acme_sales", 
                        "end_index": 10, 
                        "entity": "white_wines", 
                        "entity_value": "chardonnay", 
                        "start_index": 0, 
                        "value": "chardonnay"
                    }, 
                    {
                        "current_value": "chardonnay", 
                        "domain_key": "acme_sales", 
                        "end_index": 10, 
                        "entity": "wine varietals", 
                        "entity_value": "chardonnay", 
                        "start_index": 0, 
                        "value": "chardonnay"
                    }
                ]
````

**ES Score**

````json
"es_score": 0
````

**Featured Normalized Tokens**

````json
 "featured_normalized_tokens": "chardonnay"
````

**Featured Tokens**

````json
"featured_tokens": [
  "chardonnay"
]
````

**Featured Tokens Lemma Map**

````json
"featured_tokens_lemma_map": {
                    "chardonnay": "chardonnay"
                }
````

**Id**

````json
"id": null
````

**Intent**

````json
"intent": null
````

**Intent Id**

````json
"intent_id": null
````

**Is Transaction**

````json
"is_transaction": false
````

**Knowledge Pack Id**

````json
"knowledge_pack_id": null
````

**Negation**

Is the message one of negation: true or false. 

**New Normalized Document**

````json
"new_normalized_document": "Chardonnay"
````

**New Normalized Document Query**

````json
"new_normalized_document_query": "Chardonnay"
````

**Normalized Document**

````json
"normalized_document": "chardonnay"
````

**Normalized Tokens**

````json
"normalized_tokens": "chardonnay"
````

**Original Document**

````json
"original_document": "Chardonnay"
````

**Original Text**

````json
"original_text": "Chardonnay"
````

````json
"plain_document": "Chardonnay"
````
       
**Parts of Speech**

````json
"pos": [
 [
   "chardonnay", 
   "NN"
 ]
]
````

````json
"raw_document": "chardonnay"
````

**Score**

````json
"score": 1
````
                

**Second Best Result**

````json
"second_best_result": null
````

**Tone**

````json
"tone": ""
````

**Training Datum**

````json
"training_datum_id": null					
````

**User Information**

The user information attached to each entry is as follows:

````json
"user": {
	"display_name": "David Gwartney",
    "id": 25908
} 
````

Where the object contains two fields:

_display\_name_ - First and last name concatenated of the user conversing with the chatbot.

_id_ - Unique identifier of the user within the account


