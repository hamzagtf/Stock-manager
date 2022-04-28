def key_Events(this, e):

	if e.key() == 16777220 or e.key() == 16777221: # enter key 
			
			if this.ui.stackedWidget.currentIndex() == 7: #login page
				this.signIn(this)

			if this.ui.stackedWidget.currentIndex() == 10: # home page

				this.hp.insert_to_table(
				this.ui.h_table, 
				this.ui.h_input,
				this.ui.h_lcd)

	if e.key() == 16777219 or e.key() == 16777223: # Delete key
		if this.ui.stackedWidget.currentIndex() == 10: #home page
			this.hp.remove_row(
				this.ui.h_table, 
				this.ui.h_lcd)

		if this.ui.stackedWidget.currentIndex() == 5: # sells page
			this.sl.removeProduct(this,
					this.ui.bellTable)

		if this.ui.stackedWidget.currentIndex() == 1: #stock page
			this.sp.removeProduct(this,
				this.ui.s_table, this.ui.s_lcd)

		if this.ui.stackedWidget.currentIndex() == 0: #dbt page
			this.db.removeUser(this,this.ui.d_tableContent, this.ui.d_total )

		if this.ui.stackedWidget.currentIndex() == 2: #dbt page 2
			this.db.removeUserBell(this,this.ui.u_page_table)

		if this.ui.stackedWidget.currentIndex() == 4:
			this.admin.delete_seller(this, this.ui.table_user)