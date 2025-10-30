import tkinter as tk
from tkinter import ttk

class TopFivePost:
    title: str
    description: str
    topFive: list[str]
    likes: int
    comments: list[str]

    def __init__(self, title: str, description: str, topFive: list[str]):
        self.title = title
        self.description = description
        self.topFive = topFive
        self.likes = 0
        self.comments = []

    def displayPost(self):
        return f"{self.title}\n\n{self.description}\n\nMy top 5 are:\n" + "\n".join(
            [f"# {i+1}: {item}" for i, item in enumerate(self.topFive)]
        )

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Top Five App")
        self.posts = []

        # Create a Notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        # Create Feed Tab
        self.feed_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.feed_tab, text="Feed")
        self.feed_frame = ttk.Frame(self.feed_tab)
        self.feed_frame.pack(fill="both", expand=True)

        # Add a Scrollable Canvas for the Feed
        self.feed_canvas = tk.Canvas(self.feed_frame)
        self.scrollbar = ttk.Scrollbar(self.feed_frame, orient="vertical", command=self.feed_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.feed_canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.feed_canvas.configure(scrollregion=self.feed_canvas.bbox("all"))
        )

        self.feed_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.feed_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.feed_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Create New Post Tab
        self.new_post_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.new_post_tab, text="Create Post")
        self.create_post_ui()

    def create_post_ui(self):
        def submit_post():
            title = title_entry.get()
            description = description_entry.get()
            top_five = [entry.get() for entry in top_five_entries]

            if title and description and all(top_five):
                post = TopFivePost(title, description, top_five)
                self.posts.append(post)
                self.update_feed()
                title_entry.delete(0, tk.END)
                description_entry.delete(0, tk.END)
                for entry in top_five_entries:
                    entry.delete(0, tk.END)

        # Title Entry
        ttk.Label(self.new_post_tab, text="Title:", font=("Arial", 12)).pack(pady=5)
        title_entry = ttk.Entry(self.new_post_tab, width=40)
        title_entry.pack(pady=5)

        # Description Entry
        ttk.Label(self.new_post_tab, text="Description:", font=("Arial", 12)).pack(pady=5)
        description_entry = ttk.Entry(self.new_post_tab, width=40)
        description_entry.pack(pady=5)

        # Top Five Entries
        ttk.Label(self.new_post_tab, text="Top 5 Items:", font=("Arial", 12)).pack(pady=5)
        top_five_entries = []
        for i in range(5):
            entry = ttk.Entry(self.new_post_tab, width=40)
            entry.pack(pady=2)
            top_five_entries.append(entry)

        # Submit Button
        submit_button = ttk.Button(self.new_post_tab, text="Submit", command=submit_post)
        submit_button.pack(pady=10)

    def update_feed(self):
        # Clear the feed
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Display all posts
        for post in self.posts:
            post_frame = ttk.Frame(self.scrollable_frame, padding=10, relief="solid")
            post_frame.pack(pady=5, fill="x", expand=True)

            title_label = ttk.Label(post_frame, text=post.title, font=("Arial", 14, "bold"))
            title_label.pack(anchor="w")

            description_label = ttk.Label(post_frame, text=post.description, font=("Arial", 12))
            description_label.pack(anchor="w", pady=5)

            for i, item in enumerate(post.topFive):
                item_label = ttk.Label(post_frame, text=f"# {i+1}: {item}", font=("Arial", 12))
                item_label.pack(anchor="w")
            
            # Add like and comment section
            interaction_frame = ttk.Frame(post_frame)
            interaction_frame.pack(anchor="w", pady=(10, 0))
            
            like_count = ttk.Label(interaction_frame, text=f"❤️ {post.likes}", font=("Arial", 12))
            like_count.pack(side="left", padx=(0, 10))
            
            def like_post():
                post.likes += 1
                like_count.config(text=f"❤️ {post.likes}")
            
            like_button = ttk.Button(interaction_frame, text="Like", command=like_post)
            like_button.pack(side="left", padx=(0, 10))

            # Comment section
            def create_comment_section():
                nonlocal post_frame
                comments_frame = ttk.Frame(post_frame)
                comments_frame.pack(fill="x", pady=(5, 0))
                comments_frame.is_visible = False
                comments_frame.pack_forget()

                def toggle_comments():
                    if not comments_frame.is_visible:
                        comments_frame.pack(fill="x", pady=(5, 0))
                        toggle_button.config(text=f"Hide Comments ({len(post.comments)})")
                        comments_frame.is_visible = True
                    else:
                        comments_frame.pack_forget()
                        toggle_button.config(text=f"Show Comments ({len(post.comments)})")
                        comments_frame.is_visible = False

                def add_comment():
                    comment_text = comment_entry.get().strip()
                    if comment_text:
                        post.comments.append(comment_text)
                        comment_entry.delete(0, tk.END)
                        
                        # Update comments display
                        comment_label = ttk.Label(comments_frame, text=comment_text, 
                                               wraplength=400, font=("Arial", 10))
                        comment_label.pack(anchor="w", pady=2)
                        
                        # Update comment count on toggle button
                        toggle_button.config(text=f"Hide Comments ({len(post.comments)})")
                        
                        # Ensure comments are visible when adding a comment
                        if not comments_frame.is_visible:
                            toggle_comments()

                # Comment toggle button
                toggle_button = ttk.Button(interaction_frame, 
                                         text=f"Show Comments ({len(post.comments)})",
                                         command=toggle_comments)
                toggle_button.pack(side="left")

                return comments_frame, add_comment

            comments_frame, add_comment = create_comment_section()

            # Comment input
            comment_frame = ttk.Frame(post_frame)
            comment_frame.pack(fill="x", pady=(5, 0))
            
            comment_entry = ttk.Entry(comment_frame)
            comment_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
            
            comment_button = ttk.Button(comment_frame, text="Comment", command=add_comment)
            comment_button.pack(side="right")

            # Display existing comments
            for comment in post.comments:
                comment_label = ttk.Label(comments_frame, text=comment, 
                                        wraplength=400, font=("Arial", 10))
                comment_label.pack(anchor="w", pady=2)

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()