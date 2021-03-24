import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import 'fontsource-roboto';
import * as monaco from 'monaco-editor';

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);

// Register a new language
monaco.languages.register({ id: 'mySpecialLanguage' });

// Register a tokens provider for the language
monaco.languages.setMonarchTokensProvider('mySpecialLanguage', {
	tokenizer: {
		root: [
			[/.*SELECT|INSERT|INTO|SELECT|FROM|DURING|END|OF|BEGIN|BY|AT|IN|NEAR|ON|CAUSING|CAUSED|HAVING|TAG/i, "qtoken"],
			[/'[^'"]*'(?=(?:[^"]*"[^"]*")*[^"]*$)/,"singleQuoteString"]
		]
	}
});

// Define a new theme that contains only rules that match this language
monaco.editor.defineTheme('myCoolTheme', {
	base: 'vs',
	inherit: false,
	rules: [
		{ token: 'qtoken', foreground: '0078d7', fontStyle: 'bold' },
		{ token: "singleQuoteString", foreground: 'ff0000', fontStyle: 'italic' }
	],
});

// Register a completion item provider for the new language
monaco.languages.registerCompletionItemProvider('mySpecialLanguage', {
	provideCompletionItems: () => {
		var suggestions = [{
			label: 'simpleText',
			kind: monaco.languages.CompletionItemKind.Text,
			insertText: 'simpleText'
		}, {
			label: 'testing',
			kind: monaco.languages.CompletionItemKind.Keyword,
			insertText: 'testing(${1:condition})',
			insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet
		}, {
			label: 'ifelse',
			kind: monaco.languages.CompletionItemKind.Snippet,
			insertText: [
				'if (${1:condition}) {',
				'\t$0',
				'} else {',
				'\t',
				'}'
			].join('\n'),
			insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
			documentation: 'If-Else Statement'
		}];
		return { suggestions: suggestions };
	}
});

window.editor = monaco.editor.create(document.getElementById("queryEditorDivision"), {
	theme: 'myCoolTheme',
	value: "SELECT '<event>'\nAT '<spatial>'\nFROM'<database>'",
	language: 'mySpecialLanguage',
	lineNumbers: "on",
	automaticLayout: true,
	roundedSelection: false,
	scrollBeyondLastLine: false,
	readOnly: false,
});


// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
