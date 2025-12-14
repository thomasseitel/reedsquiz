import QtQuick
import QtQuick.Controls

ApplicationWindow {
    id: appWindow
    visible: true
    width: 800
    height: 800
    title: "Reed's Quiz"

   Connections {
        target: quiz

        function onQuizFinished() {
            appWindow.close()
        }
   }

    Rectangle {
        anchors.fill: parent
        anchors.margins: 20

        Column {
            id: mainLayout
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.top
            spacing: 20
            width: parent.width - 40

            Image {
                id: img
                property int version: 0

                Connections {
                    target: quiz
                    function onQuestionChanged() { img.version++ }
                }

                source: "image://imageprovider/live_feed?" + version
                width: 400
                height: 400
                fillMode: Image.PreserveAspectFit
                anchors.horizontalCenter: parent.horizontalCenter
            }

            Text {
                id: question
                text: quiz.question
                wrapMode: Text.WordWrap
                font.pointSize: 18
                horizontalAlignment: Text.AlignHCenter
                width: parent.width
            }

            Column {
                id: optionsContainer
                spacing: 10
                width: 400
                anchors.horizontalCenter: parent.horizontalCenter
                Repeater {
                    model: quiz.options

                    delegate: Column {
                        width: optionsContainer.width
                        spacing: 5

                        RadioButton {
                            text: modelData.answer
                            checked: modelData.selected
                            onClicked: quiz.submitAnswer(modelData.index)
                        }
                        Text {
                            wrapMode: Text.WordWrap
                        }
                    }
                }
            }

            Text {
                id: feedback
                text: quiz.feedback
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
                width: parent.width
            }
        }

        Button{
            visible: quiz.mayContinue
            text: quiz.continueText
            width: 100
            height: 50
            anchors.bottom: parent.bottom
            anchors.right: parent.right
            onClicked: quiz.nextQuestion()
        }
    }
}