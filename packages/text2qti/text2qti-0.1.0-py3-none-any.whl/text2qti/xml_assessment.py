# -*- coding: utf-8 -*-
#
# Copyright (c) 2020, Geoffrey M. Poore
# All rights reserved.
#
# Licensed under the BSD 3-Clause License:
# http://opensource.org/licenses/BSD-3-Clause
#


from .quiz import Quiz


BEFORE_ITEMS = '''\
<?xml version="1.0" encoding="UTF-8"?>
<questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/ims_qtiasiv1p2 http://www.imsglobal.org/xsd/ims_qtiasiv1p2p1.xsd">
  <assessment ident="{assessment_identifier}" title="{title}">
    <qtimetadata>
      <qtimetadatafield>
        <fieldlabel>cc_maxattempts</fieldlabel>
        <fieldentry>1</fieldentry>
      </qtimetadatafield>
    </qtimetadata>
    <section ident="root_section">
'''

AFTER_ITEMS = '''\
    </section>
  </assessment>
</questestinterop>
'''


START_ITEM = '''\
      <item ident="{question_identifier}" title="{question_title}">
'''

END_ITEM = '''\
      </item>
'''


ITEM_METADATA = '''\
        <itemmetadata>
          <qtimetadata>
            <qtimetadatafield>
              <fieldlabel>question_type</fieldlabel>
              <fieldentry>{question_type}</fieldentry>
            </qtimetadatafield>
            <qtimetadatafield>
              <fieldlabel>points_possible</fieldlabel>
              <fieldentry>{points_possible}</fieldentry>
            </qtimetadatafield>
            <qtimetadatafield>
              <fieldlabel>original_answer_ids</fieldlabel>
              <fieldentry>{original_answer_ids}</fieldentry>
            </qtimetadatafield>
            <qtimetadatafield>
              <fieldlabel>assessment_question_identifierref</fieldlabel>
              <fieldentry>{assessment_question_identifierref}</fieldentry>
            </qtimetadatafield>
          </qtimetadata>
        </itemmetadata>
'''


ITEM_PRESENTATION = '''\
        <presentation>
          <material>
            <mattext texttype="text/html">{question_xml}</mattext>
          </material>
          <response_lid ident="response1" rcardinality="Single">
            <render_choice>
{choices}
            </render_choice>
          </response_lid>
        </presentation>
'''

ITEM_PRESENTATION_CHOICE = '''\
              <response_label ident="{ident}">
                <material>
                  <mattext texttype="text/html">{choice_xml}</mattext>
                </material>
              </response_label>'''


ITEM_RESPROCESSING_START = '''\
        <resprocessing>
          <outcomes>
            <decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/>
          </outcomes>
'''

ITEM_RESPROCESSING_GENERAL_FEEDBACK = '''\
          <respcondition continue="Yes">
            <conditionvar>
              <other/>
            </conditionvar>
            <displayfeedback feedbacktype="Response" linkrefid="general_fb"/>
          </respcondition>
'''

ITEM_RESPROCESSING_CHOICE_FEEDBACK = '''\
          <respcondition continue="Yes">
            <conditionvar>
              <varequal respident="response1">{ident}</varequal>
            </conditionvar>
            <displayfeedback feedbacktype="Response" linkrefid="{ident}_fb"/>
          </respcondition>
'''

ITEM_RESPROCESSING_SET_CORRECT_WITH_FEEDBACK = '''\
          <respcondition continue="No">
            <conditionvar>
              <varequal respident="response1">{ident}</varequal>
            </conditionvar>
            <setvar action="Set" varname="SCORE">100</setvar>
            <displayfeedback feedbacktype="Response" linkrefid="correct_fb"/>
          </respcondition>
'''

ITEM_RESPROCESSING_SET_CORRECT_NO_FEEDBACK = '''\
          <respcondition continue="No">
            <conditionvar>
              <varequal respident="response1">{ident}</varequal>
            </conditionvar>
            <setvar action="Set" varname="SCORE">100</setvar>
          </respcondition>
'''

ITEM_RESPROCESSING_INCORRECT_FEEDBACK = '''\
          <respcondition continue="Yes">
            <conditionvar>
              <other/>
            </conditionvar>
            <displayfeedback feedbacktype="Response" linkrefid="general_incorrect_fb"/>
          </respcondition>
'''

ITEM_RESPROCESSING_END = '''\
        </resprocessing>
'''


ITEM_FEEDBACK_GENERAL = '''\
        <itemfeedback ident="general_fb">
          <flow_mat>
            <material>
              <mattext texttype="text/html">{feedback}</mattext>
            </material>
          </flow_mat>
        </itemfeedback>
'''

ITEM_FEEDBACK_CORRECT = '''\
        <itemfeedback ident="correct_fb">
          <flow_mat>
            <material>
              <mattext texttype="text/html">{feedback}</mattext>
            </material>
          </flow_mat>
        </itemfeedback>
'''

ITEM_FEEDBACK_INCORRECT = '''\
        <itemfeedback ident="general_incorrect_fb">
          <flow_mat>
            <material>
              <mattext texttype="text/html">&lt;p&gt;Wrong comment&lt;/p&gt;</mattext>
            </material>
          </flow_mat>
        </itemfeedback>
'''

ITEM_FEEDBACK_INDIVIDUAL = '''\
        <itemfeedback ident="{ident}_fb">
          <flow_mat>
            <material>
              <mattext texttype="text/html">{feedback}</mattext>
            </material>
          </flow_mat>
        </itemfeedback>
'''




def assessment(*, quiz: Quiz, assessment_identifier: str, title: str) -> str:
    '''
    Generate assessment XML from Quiz.
    '''
    xml = []
    xml.append(BEFORE_ITEMS.format(assessment_identifier=assessment_identifier,
                                   title=title))
    for question in quiz.questions:
        correct_choice = None
        for choice in question.choices:
            if choice.correct:
              correct_choice = choice
              break
        if correct_choice is None:
            raise TypeError

        xml.append(START_ITEM.format(question_identifier=f'text2qti_question_{question.id}',
                                     question_title=question.title_xml))

        xml.append(ITEM_METADATA.format(question_type=question.type,
                                        points_possible=question.points_possible,
                                        original_answer_ids=','.join(f'text2qti_choice_{c.id}' for c in question.choices),
                                        assessment_question_identifierref=f'text2qti_question_ref_{question.id}'))

        choices = '\n'.join(ITEM_PRESENTATION_CHOICE.format(ident=f'text2qti_choice_{c.id}', choice_xml=c.choice_xml)
                                                            for c in question.choices)
        xml.append(ITEM_PRESENTATION.format(question_xml=question.question_xml,
                                            choices=choices))

        resprocessing = []
        resprocessing.append(ITEM_RESPROCESSING_START)
        if question.feedback_raw is not None:
            resprocessing.append(ITEM_RESPROCESSING_GENERAL_FEEDBACK)
        for choice in question.choices:
            if choice.feedback_raw is not None:
                resprocessing.append(ITEM_RESPROCESSING_CHOICE_FEEDBACK.format(ident=f'text2qti_choice_{choice.id}'))
        if question.correct_feedback_raw is not None:
            resprocessing.append(ITEM_RESPROCESSING_SET_CORRECT_WITH_FEEDBACK.format(ident=f'text2qti_choice_{correct_choice.id}'))
        else:
            resprocessing.append(ITEM_RESPROCESSING_SET_CORRECT_NO_FEEDBACK.format(ident=f'text2qti_choice_{correct_choice.id}'))
        if question.incorrect_feedback_raw is not None:
            resprocessing.append(ITEM_RESPROCESSING_INCORRECT_FEEDBACK)
        resprocessing.append(ITEM_RESPROCESSING_END)
        xml.append(''.join(resprocessing))

        if question.feedback_raw is not None:
            xml.append(ITEM_FEEDBACK_GENERAL.format(feedback=question.feedback_xml))
        if question.correct_feedback_raw is not None:
            xml.append(ITEM_FEEDBACK_CORRECT.format(feedback=question.correct_feedback_xml))
        if question.incorrect_feedback_raw is not None:
            xml.append(ITEM_FEEDBACK_INCORRECT.format(feedback=question.incorrect_feedback_xml))
        for choice in question.choices:
            if choice.feedback_raw is not None:
                xml.append(ITEM_FEEDBACK_INDIVIDUAL.format(ident=f'text2qti_choice_{choice.id}',
                                                           feedback=choice.feedback_xml))

        xml.append(END_ITEM)

    xml.append(AFTER_ITEMS)

    return ''.join(xml)
