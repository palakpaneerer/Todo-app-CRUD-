# This is ToDo web application using streamlit and SQLite3.
# the functions used here is setted in dx_fxns.py.
 

# core package
import streamlit as st
import streamlit.components.v1 as stc   # for visualising the title banner

# EDA package
import pandas as pd
import plotly.express as px

# DB fanctions packages
from db_fxns import create_table, add_data, view_all_data, view_unique_tasks, get_task, edit_task_data, delete_data

# make a title banner
HTML_BANNER = """
    <div style="background-color:#464e5f;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">ToDo App (CRUD)</h1>
    <p style="color:white;text-align:center;">Built with Streamlit</p>
    </div>
    """


def main():
    # make a title on the top page
    stc.html(HTML_BANNER)
    
    # make a sidebar to select options
    menu = ["Create", "Read", "Update", "Delete", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    # If there are no tables, this code makes a new table automatically
    create_table()
    
    
    
    
    
    # make the Creat page
    if choice == "Create":
        # set the sub header
        st.subheader("Add Items")
        
        # set the page layout
        # make two areas on the main area
        col1, col2 = st.columns(2)

        # make a text input area on the left
        with col1:
            task = st.text_area("Task To Do")
        
        # make a status input area on the right
        # make a date input area on the right
        with col2:
            task_status = st.selectbox("Status", ["ToDo", "Doing", "Done"])
            task_due_date = st.date_input("Due Date")
        
        # if you push this bottun, the data in task, task_status and task_due_date will be in the database.
        if st.button("Add Task"):
            add_data(task, task_status, task_due_date)
            st.success(f"Successfully Added: {task}")
    
    
    
    
        
    # make the Read page
    elif choice == "Read":
        # set the sub header
        st.subheader("View Items")        
        
        # get all data from the database
        result = view_all_data()
        
        # this is just for confirming data contents for developper
        # st.write(result)
        
        # the data from the database will be changed dataframe format
        df = pd.DataFrame(result, columns=['Task', 'Status', 'Due Date'])
        
        # the data with dataframe format will be shown in this expander
        with st.expander("View ALL Data"):
            st.dataframe(df)
            
        with st.expander("Task Status"):
            
            # the task status will be shown in dataframe format
            task_df = df['Status'].value_counts().to_frame()
            st.dataframe(task_df)
            
            # the current state of tasks will be shown in a pie chart
            task_df = task_df.reset_index()
            p1 = px.pie(task_df, names='Status', values='count')
            st.plotly_chart(p1, use_container_width=True)           # "use_container_width" makes the pie chart fit with the web page width
            
        
        

       
    # make the Update page
    elif choice == "Update":
        # set the sub header
        st.subheader("Edit/Update Items")
    
        # the current Data will be shown in this expander
        with st.expander("Current Data"):
            
            # get all data from the databaase
            result = view_all_data()
            
            # this is just for confirming data contents for developper
            # st.write(result)
            
            # the data from the database will be changed and shown in dataframe format
            df = pd.DataFrame(result, columns=['Task', 'Status', 'Due Date'])
            st.dataframe(df)
        
        
        # this shows all unique tasks and makes them selectable in a select box
        list_of_tasks = [i[0] for i in view_unique_tasks()]
        selected_task = st.selectbox("Task",list_of_tasks)
		
        # selected task will be in task_result
        task_result = get_task(selected_task)
		
        # this is just for confirming data contents for developper
        # st.write(task_result)
        
       
        if task_result:
            # the data of the task selected above are catched here
            task = task_result[0][0]
            task_status = task_result[0][1]
            task_due_date = task_result[0][2]
            
            # set the page layout
            col1, col2 = st.columns(2)

            # make a text input area on the left to update it (default: old task's contents)
            with col1:
                new_task = st.text_area("Task To Do", task)
            
            # make a status input area on the right to update it
            # make a date input area on the right to update it
            with col2:
                new_task_status = st.selectbox(task_status, ["ToDo", "Doing", "Done"])
                new_task_due_date = st.date_input(task_due_date)
            
            # if you push this bottun, the data in the current status of the task (task, task_status and task_due_date) will be in the database.
            if st.button("Update Task"):
                edit_task_data(new_task, new_task_status, new_task_due_date, task, task_status, task_due_date)
                st.success(f"Successfully Updated :: {task} to :: {new_task}")

            # the updated data will be shown in this expander
            with st.expander("Updated Data"):
                # get the updated data from the database
                result2 = view_all_data()
                
                # this is just for confirming data contents for developper
                # st.write(result)
                
                # show the updated data in dataframe format
                df2 = pd.DataFrame(result2, columns=["Task","Status","Date"])
                st.dataframe(df2)
    
 
 
 
 
    # make the Delete page    
    elif choice == "Delete":
        # set the sub header
        st.subheader("Delete Items")
    
        # this shows the current data
        with st.expander("Current Data"):
            result = view_all_data()
            df = pd.DataFrame(result, columns=['Task', 'Status', 'Due Date'])
            st.dataframe(df)
    
    
 
        # make all unique tasks selectable in this select box
        list_of_task = [i[0] for i in view_unique_tasks()]
        selected_task = st.selectbox("Task To Delete", list_of_task)
        
        # warn to confirm the action
        st.warning(f"Do you want to Delete {selected_task}")
        
        # if the button is pushed, the selected task will be deleted in the database
        if st.button("Delete Task"):
            delete_data(selected_task)
            st.success("Task has been successflly Deleted")
    
        # show the updated data
        with st.expander("Updated Data"):
            new_result = view_all_data()
            df2 = pd.DataFrame(new_result, columns=['Task', 'Status', 'Due Date'])
            st.dataframe(df2)
    
    
    
    
    
    # make the About page
    elif choice == "About":
        st.subheader("About")

    
    





    
if __name__ == '__main__':
    main()
