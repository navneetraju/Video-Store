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


function createEditor(){
	// Register a new language
monaco.languages.register({ id: 'mySpecialLanguage' });

// Register a tokens provider for the language
monaco.languages.setMonarchTokensProvider('mySpecialLanguage', {
	tokenizer: {
		root: [
			[/.*SELECT|INSERT|INTO|SELECT|FROM|DURING|END|OF|BEGIN|BY|AT|IN|NEAR|ON|CAUSING|CAUSED|HAVING|TAG/i, "qtoken"],
			[/'[^'"]*'(?=(?:[^"]*"[^"]*")*[^"]*$)/,"singleQuoteString"],
			[/\/\/.*/,"commentString"]
		]
	}
});

// Define a new theme that contains only rules that match this language
monaco.editor.defineTheme('myCoolTheme', {
	base: 'vs',
	inherit: false,
	rules: [
		{ token: 'qtoken', foreground: '0078d7', fontStyle: 'bold' },
		{ token: "singleQuoteString", foreground: 'ff0000', fontStyle: 'italic' },
		{ token: "commentString", foreground: '229977'}
	],
});

// Register a completion item provider for the new language
monaco.languages.registerCompletionItemProvider('mySpecialLanguage', {
	provideCompletionItems: () => {
		var suggestions = [{
			label: 'SELECT',
			kind: monaco.languages.CompletionItemKind.Snippet,
			insertText: ["SELECT '<Event>'"
			].join('\n'),
			insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
			documentation: 'Experiential'
		},
		{
			label: 'FROM',
			kind: monaco.languages.CompletionItemKind.Snippet,
			insertText: ["FROM '<Database>'"
			].join('\n'),
			insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
			documentation: 'Database'
		},
		{
			label: 'HAVING TAG',
			kind: monaco.languages.CompletionItemKind.Snippet,
			insertText: ["HAVING TAG '<Information>'"
			].join('\n'),
			insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
			documentation: 'Informational'
		},
		{
			label: 'AT',
			kind: monaco.languages.CompletionItemKind.Snippet,
			insertText: ["AT '<Spatial>'"
			].join('\n'),
			insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
			documentation: 'Spatial'
		},
	];
		return { suggestions: suggestions };
	}
});
	window.editor = monaco.editor.create(document.getElementById("queryEditorDivision"), {
		theme: 'myCoolTheme',
		value: "//VetaQL Here",
		language: 'mySpecialLanguage',
		lineNumbers: "on",
		automaticLayout: true,
		roundedSelection: false,
		scrollBeyondLastLine: false,
		readOnly: false,
	});
}
export {createEditor};
// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
