/* @odoo-module */
import core from 'web.core';
import SystrayMenu from 'web.SystrayMenu';
import Widget from 'web.Widget';
import rpc from 'web.rpc';
const qweb = core.qweb;
const SystrayWidget = Widget.extend({
    template: 'IconSystrayDropdown',
    events: {
        'click .o-dropdown-button1': '_onButton1Click',
        'click .o-dropdown-button2': '_onButton2Click',
        'click .o_MessagingMenu_toggler': '_onToggleClick',
    },
    init: function (parent, options) {
        this._super(parent);
        this.worksheetData = [];
        this.userRecords = [];
        this.dropdownVisible = false;
        this.activeButton = '1';

        this.loadWorksheetData1();
        this.loadWorksheetData2();
    },
    _onToggleClick: function (ev) {
        ev.preventDefault();
        ev.stopPropagation();
        const dropBox = this.$('#systray_notif');
        this.toggleDropdownVisibility();
        this.updateContentWithData(dropBox);
    },


    toggleDropdownVisibility: function () {
        this.dropdownVisible = !this.dropdownVisible;
        const dropBox = this.$('#systray_notif');
        dropBox.toggle();
    },





    _onButton1Click: function () {
        this.toggleButton('1');
        const dropBox = this.$('#systray_notif');
        console.log('Button 1 click ok');
        this.updateContentWithData(dropBox);
    },



    _onButton2Click: function () {
    this.toggleButton('2');
    const dropBox = this.$('#systray_notif');
    console.log('Button 2 click ok');
    this.updateContentWithData(dropBox);




    const groupedUsers = {};
    this.userRecords.forEach(user => {
        if (!(user.us_name in groupedUsers)) {
            groupedUsers[user.us_name] = [];
        }
        groupedUsers[user.us_name].push(user);
    });

    $('.systray_notification').empty(); // Clear previous content

    Object.keys(groupedUsers).forEach(username => {
        const userData = groupedUsers[username];

        // Create a div to hold the table and username
        const $tableDiv = $('<div></div>').css({
            'margin-bottom': '30px', // Add space between tables
        });



        // Create a username label
        const $usernameLabel = $('<div></div>').text(username).css({
            'font-weight': 'bold',
            'margin-bottom': '7px', // Add space below username
        });
        $tableDiv.append($usernameLabel); // Append username to the div



        const $table = $('<table class="user-table"></table>').css({
            'width': '100%',
            'border-collapse': 'collapse',
            'border': '1px solid #000', // Black border around the table
            // Add additional table styles here as needed
        });



        const $thead = $('<thead></thead>').css({
            'background-color': '#71639E;',
            'font-weight': 'bold',
            'border': '1px solid #000', // Black border for thead
            'color': '#fff', // Set font color to white
            // Add additional header styles here if needed
        });
        $thead.append(`<tr>
                            <th class="highlight-header" style="border: 1px solid #000; display: none;">UserName</th>
                            <th class="highlight-header" style="border: 1px solid #000;">Name</th>
                            <th class="highlight-header" style="border: 1px solid #000;">Project</th>
                            <th class="highlight-header" style="border: 1px solid #000;">Task</th>
                            <th class="highlight-header" style="border: 1px solid #000;">Status</th>
                        </tr>`);
        $table.append($thead);

        const $tbody = $('<tbody></tbody>').css('background-color', '#f9f9f9');
        userData.forEach(user => {
            if (user.demotest !== 'done') {
                const $row = $('<tr></tr>');
                // Do not include the Username column in the table rows
                $row.append(`<td style="border: 1px solid #000; display: none;">${user.us_name}</td>`); // Hide Username column
                $row.append(`<td style="border: 1px solid #000;">${user.name}</td>`);
                $row.append(`<td style="border: 1px solid #000;">${user.proj_id}</td>`);
                $row.append(`<td style="border: 1px solid #000;">${user.task_id}</td>`);
                $row.append(`<td style="border: 1px solid #000;">${user.demotest}</td>`);
                $tbody.append($row);
            }
        });
        $table.append($tbody);

        $tableDiv.append($table); // Append table to the div
        $('.systray_notification').append($tableDiv); // Append the div to the notification area
    });
},
    updateContentWithData: function (dropBox) {
        if (this.activeButton === '1') {
            $('.systray_notification').html(qweb.render("SystrayDetails", { worksheetData: this.worksheetData }));
            this.worksheetData.forEach(user => {
                if (user.worksheet_data) {
                    const headerBackgroundColor = user.worksheet_data.some(worksheet => worksheet.odmsr_ids.some(es => es.demotest === 'working'))
                        ? '#71639E;'
                        : '#5f3f56;';
                    $('.systray_user_table:contains("' + user.user_name + '") .content table th').css('background-color', headerBackgroundColor);
                }
            });
    }
},
    loadWorksheetData1: function () {
        rpc.query({
            model: 'wiz.wiz',
            method: 'get_worksheet_data',
        }).then(result => {
            this.worksheetData = result;
            const dropBox = this.$('#systray_notif');
            this.updateContentWithData(dropBox);
        }).catch(error => {
            console.error('Error loading worksheet data:', error);
        });
    },

    loadWorksheetData2: function () {
        rpc.query({
            model: 'astask.astask',
            method: 'get_astask_data',
        }).then(result => {
            this.userRecords = result;
            const dropBox = this.$('#div_id');
            this.updateContentWithData(dropBox);
        }).catch(error => {
            console.error('Error loading astask data:', error);
        });
    },

    toggleButton: function (button) {
        this.activeButton = button;
        this.$('.o-dropdown-button1').removeClass('active');
        this.$('.o-dropdown-button2').removeClass('active');
        if (button === '1') {
            this.$('.o-dropdown-button1').addClass('active');
        } else {
            this.$('.o-dropdown-button2').addClass('active');
        }
    },

    start: function () {
        if (this.activeButton === '1') {
            this.$('.o-dropdown-button1').click();
        } else {
            this.$('.o-dropdown-button2').click();
        }

        $(document).on('click', (ev) => {
            const dropBox = this.$('#systray_notif');
            if (this.dropdownVisible && !dropBox.is(ev.target) && dropBox.has(ev.target).length === 0) {
                this.toggleDropdownVisibility();
            }
        });

        return this._super();
    },
});

SystrayMenu.Items.push(SystrayWidget);
export default SystrayWidget;



//okok