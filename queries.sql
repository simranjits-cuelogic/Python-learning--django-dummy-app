-- filter
-- Question.objects.filter(choice__votes = 3)
'SELECT "polls_question".* FROM "polls_question"
INNER JOIN "polls_choice" ON
    ("polls_question"."id" = "polls_choice"."question_id")
WHERE "polls_choice"."votes" = 2'


-- exlude()
-- Question.objects.exclude(choice__votes = 3)

'SELECT "polls_question".* FROM "polls_question"
    WHERE NOT ("polls_question"."id" IN (
        SELECT U1."question_id" AS Col1 FROM "polls_choice" U1
        WHERE U1."votes" = 1)
    )'