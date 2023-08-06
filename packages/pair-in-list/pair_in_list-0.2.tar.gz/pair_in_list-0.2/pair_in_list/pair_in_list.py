class pair_in_list:

    """
    Class including two functions to check if there are two elements in a list that add up to a specified sum:
    if_sum returns a boolean value, if_sum_print prints a statement with the two elements if they exist.
    """

    def __init__(self, given_list):
        """
        Args: The list to be checked
        """
        self.given_list = given_list

    def if_sum(self, desired_sum):
        """
        Args: The sum to be checked
        """
        # Create an empty set
        s = set()

        for i in range(0, len(self.given_list)):
            temp = desired_sum - self.given_list[i]
            if (temp in s):
                return True
            s.add(self.given_list[i])

        return False

    def if_sum_print(self, desired_sum):
        """
        Args: The sum to be checked
        """
        # Create an empty set
        s = set()

        for i in range(0, len(self.given_list)):
            temp = desired_sum - self.given_list[i]
            if (temp in s):
                print ("Pair with sum " + str(desired_sum) + " is (" + str(self.given_list[i]) + ", " + str(temp) + ")")
                pass
            s.add(self.given_list[i] )


def if_sum(given_list, desired_sum):
    """
    Args: The sum to be checked
    """
    # Create an empty set
    s = set()

    for i in range(0, len(given_list)):
        temp = desired_sum - given_list[i]
        if (temp in s):
            return True
        s.add(given_list[i])

    return False
