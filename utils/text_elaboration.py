import cohere
from cohere.classify import Example 

with open("keys/cohere.txt") as f:
    key = f.read()
    if not key:
        raise Exception("Add keys/openai.txt for specifying the key")
    co = cohere.Client(key.strip("\n"))
    f.close()

def summarize(text):
    prompt = """Summarize meeting: Is Wordle getting tougher to solve? Players seem to be convinced that the game has gotten harder in recent weeks ever since The New York Times bought it from developer Josh Wardle in late January. The Times has come forward and shared that this likely isn’t the case. That said, the NYT did mess with the back end code a bit, removing some offensive and sexual language, as well as some obscure words There is a viral thread claiming that a confirmation bias was at play. One Twitter user went so far as to claim the game has gone to “the dusty section of the dictionary” to find its latest words.

Summary: This meeting talks about Wordle, the game's users are upset because they state that lately the game got harder, NYT, its new owner, says they modified the source code but have not increased the difficulty.
--
Summarize meeting: The Library of Babel is a place for scholars to do research, for artists and writers to seek inspiration, for anyone with curiosity or a sense of humor to reflect on the weirdness of existence - in short, it’s just like any other library. If completed, it would contain every possible combination of 1,312,000 characters, including lower case letters, space, comma, and period. Thus, it would contain every book that ever has been written, and every book that ever could be - including every play, every song, every scientific paper, every legal decision, every constitution, every piece of scripture, and so on. At present it contains all possible pages of 3200 characters, about 104677 books.

Summary: This meeting talks about the Library of Babel, it describes it and talks about the number of books present.
--
Summarize meeting: If markets were either completely isolated by or integrated across borders, there would be little room for international business strategy to have content distinctive from ‘mainstream’ strategy. But a review of the economic evidence about the international integration of markets indicates that we fall in between these extremes, into a state of incomplete cross-border integration that I refer to as semiglobalization. More specifically, most measures of market integration have scaled new heights in the last few decades, but still fall far short of economic theory's ideal of perfect integration.

Summary: This meeting talks about international business strategies, it tells how the cross-border integration is still incomplete and how the markets are still far from the ideal of perfect integration.
--
Summarize meeting:"""
    coinput = f"{prompt}{text}\n\nSummary:"
    length = int(len(text) / 10)
    if length < 100:
        length = 100
    if length > 1024:
        length = 1024
    prediction = co.generate(model='large', prompt=coinput, max_tokens=length)
    if prediction:
        return prediction.generations[0].text.split('-')[0]
    else:
        return "Error try again!"

def extract_tasks(text):
    prompt = """Extract tasks: Is Wordle getting tougher to solve? Players seem to be convinced that the game has gotten harder in recent weeks ever since The New York Times bought it from developer Josh Wardle in late January. In the meanwhile, Teo you have to send the documents tonight. The Times has come forward and shared that this likely isn’t the case. That said, the NYT did mess with the back end code a bit, removing some offensive and sexual language, as well as some obscure words. There is a viral thread claiming that a confirmation bias was at play. One Twitter user went so far as to claim the game has gone to “the dusty section of the dictionary” to find its latest words. We need to find a solution for 

Tasks: Teo has to send the documents tonight. We need to find a solution for the viral thread anout the confirmation bias.
--
Extract tasks: Before starting, someone should turn on the lights we narrow down the connotation of Web3 by separating it from high-level controversy argues and, instead, focusing on its protocol, architecture, and evaluation from the perspective of blockchain fields. Therefore, attention has to be placed on these exact aspects. Specifically, we have identified all potential architectural design types and evaluated each of them by employing the scenario-based architecture evaluation method. Apparently the existing applications are neither secure nor adoptable as claimed. Meanwhile, we should discuss opportunities and challenges surrounding the Web3 space and answer several prevailing questions from communities.

Tasks: Someone should turn on the lights. We should discuss opportunities and challenges surrounding the Web3 space.
--
Extract tasks: If markets were either completely isolated by or integrated across borders, there would be little room for international business strategy to have content distinctive from ‘mainstream’ strategy. But a review of the economic evidence about the international integration of markets indicates that we fall in between these extremes, into a state of incomplete cross-border integration that I refer to as semiglobalization. More specifically, most measures of market integration have scaled new heights in the last few decades, but still fall far short of economic theory's ideal of perfect integration, issue which we have to address.

Tasks: We have to discuss about market integration.
--
Extract tasks:"""
    coinput = f"{prompt}{text}\n\nTasks:"
    prediction = co.generate(model='large', num_generations=5, prompt=coinput, p=0.9, max_tokens=100)
    if prediction:
        # Splitting every result into sentences and classify them
        results = []
        for sentences in [gen.text.split(".") for gen in prediction.generations]:
            sentences = list(filter(None, sentences))
            classif = co.classify(model='large',
            examples=[Example("We have to create a calendar", "Yes"), Example("Are we going to buy that cake", "No"), Example("Hello, welcome everyone", "No"), Example("We introduce with the announcements", "No"), Example("The weather is going to get worse", "No"), Example("In a week there is going to be a festival", "No"), Example("We are young", "No"), Example("You have to engineer this product", "Yes"), Example("We did a lot of stuff", "No"), Example("You are my friend", "No"), Example("Yesterday it was raining", "No"), Example("Since the jar is very old we should throw it away", "Yes")],
            inputs=sentences)
            results.append([cl.prediction for cl in classif])
        # Find the result with the most sentences classified as tasks
        accuracies = []
        for r in results:
            accuracies.append(sum(["Yes" in pred for pred in r]))
        # Return none if no sentence is classified as task
        if max(accuracies) == 0:
            return "None"
        best = accuracies.index(max(accuracies))
        # Delete sentences classified as not tasks
        n = 0
        while n < len(results[best]):
            if results[best][n] == "No":
                prediction.generations.pop(n)
                results[best].pop(n)
                continue
            n += 1
        return prediction.generations[best].text.split('\n')[0]
    else:
        return "Error try again!"


def q_a(text):
    sentences_questions = [sentence for sentence in text.split(".") if "?" in sentence]
    questions = [s.split("?")[:-1] for s in sentences_questions]
    answers = [s.split("?")[-1:] for s in sentences_questions]
    return questions, answers
