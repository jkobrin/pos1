import React from 'react';
import ReactDOM from 'react-dom';

import JqxSplitter from '../../../jqwidgets-react/react_jqxsplitter.js';
import JqxTree from '../../../jqwidgets-react/react_jqxtree.js';

class App extends React.Component {
    componentDidMount() {
        this.refs.jqxTree.on('select', (event) => {
            document.getElementById('ContentPanel').innerHTML = '<div style="margin: 10px;">' + event.args.element.id + '</div>';
        });
    }
    render() {
        let treeHTML = `
          <ul>
                <li id='Mail' item-expanded='true'>
                    <img style='float: left; margin-right: 5px;' src='../../images/mailIcon.png' /><span
                        item-title='true'>Mail</span>
                    <ul>
                        <li id='Calendar' item-expanded='true'>
                            <img style='float: left; margin-right: 5px;' src='../../images/calendarIcon.png' /><span
                                item-title='true'>Calendar</span> </li>
                        <li id='Contacts'>
                            <img style='float: left; margin-right: 5px;' src='../../images/contactsIcon.png' /><span
                                item-title='true'>Contacts</span> </li>
                        <li id='Inbox'>
                            <img style='float: left; margin-right: 5px;' src='../../images/folder.png' /><span
                                item-title='true'> <span>Inbox</span><span style='color: Blue;'> (3)</span></span>
                            <ul>
                                <li id='jQWidgets'>
                                    <img style='float: left; margin-right: 5px;' src='../../images/folder.png' /><span
                                        item-title='true'>jQWidgets</span>
                                    <ul>
                                        <li id='Admin'>
                                            <img style='float: left; margin-right: 5px;' src='../../images/folder.png' /><span
                                                item-title='true'>Admin</span> </li>
                                        <li id='Corporate'>
                                            <img style='float: left; margin-right: 5px;' src='../../images/folder.png' /><span
                                                item-title='true'>Corporate</span> </li>
                                        <li id='Finance'>
                                            <img style='float: left; margin-right: 5px;' src='../../images/folder.png' /><span
                                                item-title='true'>Finance</span> </li>
                                        <li id='Other'>
                                            <img style='float: left; margin-right: 5px;' src='../../images/folder.png' /><span
                                                item-title='true'>Other</span> </li>
                                    </ul>
                                </li>
                                <li id='Personal'>
                                    <img style='float: left; margin-right: 5px;' src='../../images/folder.png' /><span
                                        item-title='true'>Personal</span> </li>
                            </ul>
                        </li>
                        <li id='Deleted Items' item-expanded='true'>
                            <img style='float: left; margin-right: 5px;' src='../../images/recycle.png' /><span
                                item-title='true'> <span>Deleted Items</span><span style='color: Blue;'> (10)</span></span>
                            <ul>
                                <li id='Today'>
                                    <img style='float: left; margin-right: 5px;' src='../../images/folder.png' /><span
                                        item-title='true'>Today</span> </li>
                                <li id='Last Week'>
                                    <img style='float: left; margin-right: 5px;' src='../../images/folder.png' /><span
                                        item-title='true'>Last Week</span> </li>
                                <li id='Last Month'>
                                    <img style='float: left; margin-right: 5px;' src='../../images/folder.png' /><span
                                        item-title='true'>Last Month</span> </li>
                            </ul>
                            <li id='Notes'>
                                <img style='float: left; margin-right: 5px;' src='../../images/notesIcon.png' /><span
                                    item-title='true'>Notes</span> </li>
                            <li id='Settings'>
                                <img style='float: left; margin-right: 5px;' src='../../images/settings.png' /><span
                                    item-title='true'>Settings</span> </li>
                            <li id='Favorites'>
                                <img style='float: left; margin-right: 5px;' src='../../images/favorites.png' /><span
                                    item-title='true'>Favorites</span> </li>
                        </li>
                    </ul>
                </li>
            </ul>
        `;
        return (
            <JqxSplitter ref='mainSplitter'
                width={850} height={400}
                panels={[{ size: 250 }]}
            >
                <div>
                    <JqxTree style={{ border: 'none' }}
                        ref='jqxTree'
                        template={treeHTML}
                        width={'100%'} height={'100%'}
                    />
                </div>
                <div id='ContentPanel'>
                </div>
           </JqxSplitter>
        )
    }
}

ReactDOM.render(<App />, document.getElementById('app'));
