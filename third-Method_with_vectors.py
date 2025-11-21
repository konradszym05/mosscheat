import lcs
import moss

merge_git = """
void merge(vector<int>& arr, int left, int mid, int right) {
    int n1 = mid - left + 1;
    int n2 = right - mid;
    vector<int> L(n1), R(n2);

    for (int i = 0; i < n1; i++) L[i] = arr[left + i];
    for (int j = 0; j < n2; j++) R[j] = arr[mid + 1 + j];

    int i = 0, j = 0, k = left;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i]; i++;
        } else {
            arr[k] = R[j]; j++;
        }
        k++;
    }
    while (i < n1) { arr[k] = L[i]; i++; k++; }
    while (j < n2) { arr[k] = R[j]; j++; k++; }
}

void mergeSort(vector<int>& arr, int left, int right) {
    if (left >= right) return;
    int mid = left + (right - left) / 2;
    mergeSort(arr, left, mid);
    mergeSort(arr, mid + 1, right);
    merge(arr, left, mid, right);
}

"""

merge_fake = """
void merge(vector<int>& arr, int left_arg, int mid_arg, int right_arg) {
    int left[1] = {left_arg};
    int mid[1] = {mid_arg};
    int right[1] = {right_arg};

    
    int n1[1]; 
    n1[0] = mid[0] - left[0] + 1;
    
    int n2[1];
    n2[0] = right[0] - mid[0];

    vector<int> L(n1[0]), R(n2[0]);

    for (int i = 0; i < n1[0]; i++) L[i] = arr[left[0] + i];
    for (int j = 0; j < n2[0]; j++) R[j] = arr[mid[0] + 1 + j];

    int i[1] = {0};
    int j[1] = {0};
    int k[1] = {left[0]};

    while (i[0] < n1[0] && j[0] < n2[0]) {
       
        if (L[i[0]] <= R[j[0]]) {
            arr[k[0]] = L[i[0]];
            i[0]++;
        } else {
            arr[k[0]] = R[j[0]];
            j[0]++;
        }
        k[0]++;
    }

    while (i[0] < n1[0]) {
        arr[k[0]] = L[i[0]];
        i[0]++; k[0]++;
    }
    while (j[0] < n2[0]) {
        arr[k[0]] = R[j[0]];
        j[0]++; k[0]++;
    }
}

void mergeSort(vector<int>& arr, int left_arg, int right_arg) {
    int left[1] = {left_arg};
    int right[1] = {right_arg};

    if (left[0] >= right[0]) return;

    int mid[1];
    mid[0] = left[0] + (right[0] - left[0]) / 2;

    mergeSort(arr, left[0], mid[0]);
    mergeSort(arr, mid[0] + 1, right[0]);
    merge(arr, left[0], mid[0], right[0]);
}
"""

mos = moss.MossDetector.compute_similarity(merge_git, merge_fake, "cc", "merge", "merge_with_vecs")
print(mos)

ls = lcs.compute_lcs(merge_git, merge_fake)
print(ls)