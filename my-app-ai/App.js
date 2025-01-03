import React, { useState } from 'react';
import { StyleSheet, View, TextInput, Button, FlatList, Text } from 'react-native';

const API_KEY = 'sk-77092a6a28ba4e4c97d94a816d618e39';

const App = () => {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');

  const sendMessage = async () => {
    if (!inputText.trim()) return;

    // 添加用户消息
    setMessages(prev => [...prev, { role: 'user', content: inputText }]);
    setInputText('');

    try {
      const response = await fetch('https://api.deepseek.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${API_KEY}`
        },
        body: JSON.stringify({
          model: 'deepseek-chat',
          messages: [
            ...messages,
            { role: 'user', content: inputText }
          ],
          stream: false
        })
      });

      const data = await response.json();
      const aiMessage = data.choices[0].message.content;

      // 添加AI回复
      setMessages(prev => [...prev, { role: 'assistant', content: aiMessage }]);
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, { role: 'assistant', content: '请求失败，请稍后重试' }]);
    }
  };

  return (
    <View style={styles.container}>
      <FlatList
        data={messages}
        renderItem={({ item }) => (
          <View style={[
            styles.message,
            item.role === 'user' ? styles.userMessage : styles.aiMessage
          ]}>
            <Text style={styles.messageText}>{item.content}</Text>
          </View>
        )}
        keyExtractor={(item, index) => index.toString()}
        contentContainerStyle={styles.messagesContainer}
      />
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          value={inputText}
          onChangeText={setInputText}
          placeholder="输入消息..."
        />
        <Button title="发送" onPress={sendMessage} />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#f5f5f5'
  },
  messagesContainer: {
    flexGrow: 1,
    justifyContent: 'flex-end'
  },
  message: {
    maxWidth: '80%',
    padding: 12,
    borderRadius: 8,
    marginBottom: 8
  },
  userMessage: {
    alignSelf: 'flex-end',
    backgroundColor: '#007bff',
  },
  aiMessage: {
    alignSelf: 'flex-start',
    backgroundColor: '#ffffff',
  },
  messageText: {
    color: '#333333'
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 16
  },
  input: {
    flex: 1,
    borderWidth: 1,
    borderColor: '#cccccc',
    borderRadius: 8,
    padding: 8,
    marginRight: 8,
    backgroundColor: '#ffffff'
  }
});

export default App;
