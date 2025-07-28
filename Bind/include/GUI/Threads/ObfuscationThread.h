#pragma once

#include <QThread>
#include <QStringList>
#include <functional>

class ObfuscationThread : public QThread {
    Q_OBJECT

public:
    explicit ObfuscationThread(QObject* parent = nullptr);
    void setOutputCallback(std::function<void(const QString&)> callback);

signals:
    void obfuscationStarted();
    void obfuscationFinished(bool success, const QString& message);
    void progressUpdated(const QString& status);

protected:
    void run() override;

private:
    std::function<void(const QString&)> outputCallback;
}; 