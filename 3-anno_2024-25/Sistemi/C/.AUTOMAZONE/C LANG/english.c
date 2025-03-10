#include <stdio.h>
#include <string.h>
char frasi[19][100] = {
    "Last night I ... (lose) my keys",
    "I ... (visit) Paris three times.",
    "Last year I ... (visit) Paris.",
    "I ... (know) my great grandmother for a few years - she died when I was eight.",
    "I ... (know) Julie for three years - we still meet once a month.",
    "I ... (play) Hockey since I was a child - I'm pretty good!",
    "She ... (play) hockey at school but she didn't like it.",
    "Sorry, I ... (miss) the bus - I'm going to be late.",
    "I ... (miss) the bus and then I ... (miss) the aeroplane as well!",
    "Last month I ... (go) to Scotland.",
    "I'm sorry, John isn't here now. He ... (go) to the shops.",
    "We ... (finish) this room last week.",
    "I ... (finish) my exams finally - I'm so happy!",
    "Yesterday, I ... (see) all of my friends. It was great.",
    "I ... (see) Julie three times this week.",
    "She ... (live) in London since 1994.",
    "She ... (live) in London when she was a child.",
    "I ... (drink) three cups of coffee today.",
    "I ... (drink) three cups of coffee yesterday."
};

char answers[19][20] = {
    "lost",
    "have visited",
    "visited",
    "knew",
    "have known",
    "have played",
    "played",
    "have missed",
    "missed",
    "went",
    "has gone",
    "finished",
    "have finished",
    "saw",
    "have seen",
    "has lived",
    "lived",
    "have drunk",
    "drank"
};
int main() {
    int i;
    int score = 0;
    for (i = 0; i < 19; i++) {
        char answer[40] = {""};
        printf("%s\n", frasi[i]);
        fflush(stdin); 
        scanf("%s", answer);
        if (strcmp(answer, answers[i]) == 0) {
            score++;
        } else if (strcmp(answer, "exit") == 0) {
            break;
        } else {
            printf("Wrong! The correct answer is %s\n", answers[i]);
        }
        
    }
    printf("Your score is %d\n", score);
    return 0;   
}

