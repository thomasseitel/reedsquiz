import QtQuick
import QtQuick.Controls

ApplicationWindow {
    visible: true
    width: 800
    height: 800
    title: "Reed's Quiz"

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
                source: quiz.mainImage
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
    }
}