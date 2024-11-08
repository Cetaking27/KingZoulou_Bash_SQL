import sqlite3

db_path = 'electus.db'
ignored_count = 0  # Initialize ignored votes counter

with sqlite3.connect(db_path) as connectors:
    try:
        cursor = connectors.cursor()
     
        # Open and read the votes file
        with open('votes.txt', 'r') as votes_file:
            for line in votes_file:
                line = line.strip()  # Strip whitespace
                name, state, vote = line.split(';')  # Split line by ';'
                firstname, lastname = name.split(' ')  # Split first and last names
                
                # Check if voter exists in the database
                cursor.execute('SELECT id FROM voters WHERE firstname = ? AND lastname = ?', (firstname, lastname))
                voter = cursor.fetchone()
                
                if voter:
                    # Insert vote if the voter exists
                    cursor.execute('INSERT INTO votes(candidate) VALUES (?)', (vote,))
                else:
                    ignored_count += 1  # Increment ignored count if voter is not found
                    print(f'Vote of {firstname} {lastname} ignored.')
        
        connectors.commit()  # Commit all changes
        
        # Count votes for each candidate
        cursor.execute('SELECT candidate, COUNT(*) FROM votes GROUP BY candidate')
        results = cursor.fetchall()
        
        # Store results in a dictionary
        votes_count = {row[0]: row[1] for row in results}
        
        # Retrieve votes for specific candidates
        trump_votes = votes_count.get('T', 0)
        kamala_votes = votes_count.get('K', 0)
        
        # Display results
        print(f'Number of votes for Trump: {trump_votes}')
        print(f'Number of votes for Kamala: {kamala_votes}')
        print(f'Number of votes ignored: {ignored_count}')
        
        # Determine the winner
        if trump_votes > kamala_votes:
            print('Trump is elected president!')
        elif trump_votes < kamala_votes:
            print('Kamala is the president!')
        else:
            print('There are no winners, proceeding to a second round.')
            
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        connectors.rollback()
