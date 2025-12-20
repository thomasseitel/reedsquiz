import QtQuick
import QtQuick.Controls

ApplicationWindow {
    id: appWindow
    visible: true
    width: 1000
    height: 600
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

        Image {
            id: img
            property int version: 0

            Connections {
                target: quiz
                function onQuestionChanged() { img.version++ }
            }

            source: "image://imageprovider/live_feed?" + version
            width: 400
            fillMode: Image.PreserveAspectFit
            anchors.right: parent.right
        }

        Column {
            id: mainLayout
            anchors.left: parent.left
            anchors.top: img.top
            spacing: 20
            width: parent.width - img.width

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