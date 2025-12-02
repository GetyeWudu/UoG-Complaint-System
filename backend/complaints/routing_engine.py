"""
Routing engine for automatic complaint assignment based on rules
"""
from .models import RoutingRule, Complaint, Category, SubCategory
from accounts.models import Department, Campus, CustomUser
from django.db.models import Q


def auto_route_complaint(complaint):
    """
    Automatically route a complaint based on routing rules and category.
    Returns: (assigned_department, assigned_user, priority, routing_notes)
    """
    if not complaint:
        return None, None, None, "No complaint provided"
    
    routing_notes = []
    assigned_department = None
    assigned_user = None
    priority = complaint.priority
    
    # Get active routing rules, ordered by priority (highest first)
    rules = RoutingRule.objects.filter(is_active=True).order_by('-priority')
    
    # Try to match rules
    for rule in rules:
        match = True
        match_notes = []
        
        # Check category match
        if rule.category:
            if complaint.category != rule.category:
                match = False
            else:
                match_notes.append(f"Category: {rule.category.name}")
        
        # Check subcategory match
        if rule.sub_category and match:
            if complaint.sub_category != rule.sub_category:
                match = False
            else:
                match_notes.append(f"Subcategory: {rule.sub_category.name}")
        
        # Check campus match
        if rule.campus and match:
            if complaint.campus != rule.campus:
                match = False
            else:
                match_notes.append(f"Campus: {rule.campus.name}")
        
        # If rule matches, apply it
        if match:
            routing_notes.append(f"Matched rule: {rule.name} ({', '.join(match_notes)})")
            
            # Assign to department if specified
            if rule.assign_to_department:
                assigned_department = rule.assign_to_department
                routing_notes.append(f"Assigned to department: {assigned_department.name}")
            
            # Assign to user if specified
            if rule.assign_to_user:
                assigned_user = rule.assign_to_user
                routing_notes.append(f"Assigned to user: {assigned_user.username}")
            
            # Set priority if specified
            if rule.set_priority:
                priority = rule.set_priority
                routing_notes.append(f"Priority set to: {priority}")
            
            # First matching rule wins (due to priority ordering)
            break
    
    # Fallback: Route based on category if no rule matched
    if not assigned_department and not assigned_user:
        assigned_department = route_by_category(complaint)
        if assigned_department:
            routing_notes.append(f"Fallback routing by category to: {assigned_department.name}")
    
    # Final fallback: Route to complaint's department if available
    if not assigned_department and not assigned_user and complaint.department:
        assigned_department = complaint.department
        routing_notes.append(f"Fallback routing to complaint's department: {assigned_department.name}")
    
    notes = "; ".join(routing_notes) if routing_notes else "No routing rules matched"
    
    return assigned_department, assigned_user, priority, notes


def route_by_category(complaint):
    """
    Route complaint based on category mapping.
    Returns: Department or None
    """
    if not complaint.category:
        return None
    
    category_name = complaint.category.name.lower()
    
    # Category to department mapping
    category_mapping = {
        'academic': lambda: get_department_by_name('Academic Affairs'),
        'facilities': lambda: get_department_by_name('Maintenance'),
        'facility': lambda: get_department_by_name('Maintenance'),
        'infrastructure': lambda: get_department_by_name('Maintenance'),
        'it': lambda: get_department_by_name('IT Services'),
        'network': lambda: get_department_by_name('IT Services'),
        'security': lambda: get_department_by_name('Security'),
        'safety': lambda: get_department_by_name('Security'),
        'administrative': lambda: get_department_by_name('Administration'),
        'finance': lambda: get_department_by_name('Finance'),
        'bursar': lambda: get_department_by_name('Finance'),
        'housing': lambda: get_department_by_name('Housing'),
        'accommodation': lambda: get_department_by_name('Housing'),
        'health': lambda: get_department_by_name('Health Services'),
        'medical': lambda: get_department_by_name('Health Services'),
        'library': lambda: get_department_by_name('Library'),
        'transport': lambda: get_department_by_name('Transportation'),
        'transportation': lambda: get_department_by_name('Transportation'),
        'hr': lambda: get_department_by_name('Human Resources'),
    }
    
    # Try exact match
    if category_name in category_mapping:
        dept = category_mapping[category_name]()
        if dept:
            return dept
    
    # Try partial match
    for key, getter in category_mapping.items():
        if key in category_name:
            dept = getter()
            if dept:
                return dept
    
    return None


def get_department_by_name(name):
    """Helper to get department by name (case-insensitive)"""
    try:
        return Department.objects.filter(name__icontains=name).first()
    except:
        return None


def get_triage_inbox_users():
    """
    Get users who can handle triage (manual assignment).
    Typically admins, department heads, or designated triage staff.
    """
    return CustomUser.objects.filter(
        Q(role='admin') | 
        Q(role='super_admin') | 
        Q(role='dept_head')
    ).filter(is_active=True)


def suggest_routing(complaint):
    """
    Suggest routing for a complaint (used for manual review).
    Returns dict with suggestions.
    """
    dept, user, priority, notes = auto_route_complaint(complaint)
    
    return {
        'suggested_department': dept.id if dept else None,
        'suggested_department_name': dept.name if dept else None,
        'suggested_user': user.id if user else None,
        'suggested_user_name': user.get_full_name() if user else None,
        'suggested_priority': priority,
        'routing_notes': notes,
        'confidence': 'high' if dept or user else 'low'
    }

